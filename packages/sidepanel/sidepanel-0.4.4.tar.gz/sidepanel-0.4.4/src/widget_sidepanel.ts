import { JupyterLab } from "@jupyterlab/application";
import { MainAreaWidget } from '@jupyterlab/apputils';

import { DOMWidgetView, ViewList, WidgetModel, WrappedError } from '@jupyter-widgets/base';
import { BoxModel} from '@jupyter-widgets/controls';

import { find } from '@phosphor/algorithm';
import { UUID } from '@phosphor/coreutils';
import { Message, MessageLoop } from '@phosphor/messaging';
import { Widget } from '@phosphor/widgets';

import * as $ from 'jquery';

import { EXTENSION_SPEC_VERSION } from "./version";

import { SidePanel } from './sidepanel';
import '../css/SidePanel.css';

const MODULE_NAME = 'sidepanel';

export class SidePanelModel extends BoxModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: 'SidePanelModel',
      _model_module: MODULE_NAME,
      _model_module_version: EXTENSION_SPEC_VERSION,

      _view_name: 'SidePanel',
      _view_module: MODULE_NAME,
      _view_module_version: EXTENSION_SPEC_VERSION,

      title: 'SidePanel',
      side: 'split-right',
      ref: null,

      _ctrls: {}
    }
  }

  initialize(attributes: any, options: any) {
    super.initialize(attributes, options);
    this.widget_manager.display_model(undefined, this, {});
  }

  static serializers: any = {
    ...BoxModel.serializers,
  };
}

export class SidePanelView extends DOMWidgetView {
  constructor(options: any) {
    super(options);
    this.app = options.app;
  }

  _createElement(tagName: string) {
    this.pWidget = new SidePanelWidget({view: this});
    return this.pWidget.node;
  }

  _setElement(el: HTMLElement) {
    if (this.el || el !== this.pWidget.node) {
      throw new Error('Cannot reset the DOM element.');
    }

    this.el = this.pWidget.node;
    this.$el = $(this.pWidget.node);
  }

  initialize(parameters: any) {
    super.initialize(parameters);
    this.children_views = new ViewList(this.add_child_view, this.remove_child_view, this);
    this.listenTo(this.model, 'change:children', () => this.updateChildren());
    this.listenTo(this.model, 'change:_ctrls', () => this.update_ctrls());
  }

  render() {
    super.render();

    let panel = this.pWidget;
    panel.addClass('jupyter-widgets');
    panel.addClass('sidepanel');
    panel.addClass('widget-container');

    panel.removeRequest.connect((sender, idx) => {
      if (!this.updatingChildren) {
        let child = this.model.get('children')[idx];
        let children = this.model.get('children').filter((e: any, i: number) => i != idx);
        this.model.set('children', children);

        let ctrls = this.model.get('_ctrls');
        delete ctrls[child.model_id];

        this.model.sync('patch', this.model, {attrs: {_ctrls: ctrls}});
        this.touch();
      }
    });

    this.children_views.update(this.model.get('children'))
      .then(() => this.update_ctrls());

    let w = new MainAreaWidget({content: this.pWidget});
    w.id = `SidePanel-${UUID.uuid4()}`;
    w.title.label = this.model.get('title') || '';
    w.title.closable = true;

    let shell = this.app.shell;

    let ref_id: any = null;
    let label = this.model.get('ref');
    if (label) {
      let ref = find(shell.widgets('main'), w => w.title.label == label);
      if (ref) ref_id = ref.id;
    }
    shell.add(w, 'main', {mode: this.model.get('side'), ref: ref_id});
  }

  updateChildren() {
    this.updatingChildren = true;
    let children = this.model.get('children');
    this.children_views.update(children);
    this.updatingChildren = false;
  }

  update_ctrls() {
    if (this.updatingChildren) return;
    let items = this.pWidget.itemWidgets;
    let children = this.model.get('children');
    let ctrls = this.model.get('_ctrls');
    for (let i = 0; i < items.length; i++) {
      let ctrl = ctrls[children[i].model_id];
      if (ctrl !== void 0) {
        let item = items[i];
        item.widget.title.label = ctrl[0];
        item.collapsed = !ctrl[1];
        item.expand(ctrl[2]);
      }
    }
  }

  remove_child_view(view: DOMWidgetView) {
    this.pWidget.removeWidget(view.pWidget);
    view.remove();
  }

  add_child_view(model: WidgetModel, index: number) {
    // Placeholder widget to keep our position in the panel while we create the view.
    let panel = this.pWidget;
    let placeholder = new Widget();
    let ctrls = this.model.get('_ctrls');
    let ctrl = ctrls[model.model_id];

    placeholder.title.label =  ctrl && ctrl[0] || '';
    panel.addWidget(placeholder);

    return this.create_child_view(model).then((view: DOMWidgetView) => {
      let widget = view.pWidget;
      widget.title.label = placeholder.title.label;
      let item = panel.itemWidgets[panel.indexOf(placeholder)];
      item.widget = widget;
      placeholder.dispose();
      return view;
    }).catch(reject('Could not add child view to box', true));
  }

  remove() {
    this.children_views = null;
    super.remove();
  }

  processPhosphorMessage(msg: Message): void {
    super.processPhosphorMessage(msg);
    if (msg.type == 'resize') {
      for (let view of this.pWidget.itemWidgets) {
        MessageLoop.postMessage(view, Widget.ResizeMessage.UnknownSize);
      }
    }
  }

  app: JupyterLab;
  children_views: ViewList<DOMWidgetView>;
  pWidget: SidePanel;
  updatingChildren: boolean;
}

export function reject(message: any, log: any) {
  return function promiseRejection(error: any) {
    let wrapped_error = new WrappedError(message, error);
    if (log) {
      console.error(wrapped_error);
    }
    return Promise.reject(wrapped_error);
  };
}

export class SidePanelWidget extends SidePanel {
  constructor(options: any) {
    let view = options.view;
    delete options.view;
    super(options);
    this._view = view;
  }

  /**
   * Process the phosphor message.
   *
   * Any custom phosphor widget used inside a Jupyter widget should override
   * the processMessage function like this.
   */
  processMessage(msg: Message) {
    super.processMessage(msg);
    this._view.processPhosphorMessage(msg);
  }

  /**
   * Dispose the widget.
   *
   * This causes the view to be destroyed as well with 'remove'
   */
  dispose() {
    if (this.isDisposed) {
      return;
    }
    super.dispose();
    if (this._view) {
      this._view.remove();
    }
    this._view = null;
  }

  private _view: DOMWidgetView;
}

