import { ArrayExt } from '@phosphor/algorithm';

import { ISignal, Signal } from '@phosphor/signaling';
import { Panel, PanelLayout, Widget, Title } from '@phosphor/widgets';


const PANEL_ITEM_CLASS = 'sp-item';
const PANEL_ITEM_HEADER_CLASS = 'sp-item-header';
const PANEL_ITEM_CONTENTS_CLASS = 'sp-item-contents';
const PANEL_ITEM_CLASS_OPEN = 'sp-item-open';
const PANEL_ITEM_CLASS_EXPAND = 'sp-item-content-expand';

class Button extends Widget {
  constructor(options?:any) {
    super(options);
    this.addClass('sp-item-button');
    this.add(options.cls);
  }

  add(cls:string) {
    for (let c of (cls || '').split(' ')) {
      this.addClass(c);
    }
  }

  remove(cls:string) {
    for (let c of (cls || '').split(' ')) {
      this.removeClass(c);
    }
  }

  enable() {
    this._disabled = false;
    this.removeClass('disabled');
  }

  disable() {
    this._disabled = true;
    this.addClass('disabled');
  }

  _disabled: boolean = false;
}

class ToggleButton extends Button {
  constructor(options?:any) {
    super(options);
    this.state = options.state || options.state == undefined;
    this.on_cls = options.on;
    this.off_cls = options.off;
    if (this.state) this.on();
    else this.off();

    this.node.onclick = () => this.toggle();
  }

  on() {
    this.state = true;
    this.add(this.on_cls);
    this.remove(this.off_cls);
  }

  off() {
    this.state = false;
    this.remove(this.on_cls);
    this.add(this.off_cls);
  }

  toggle() {
    if (this._disabled) return;
    if (this.state) this.off();
    else this.on();
    this._clicked.emit(this.state);
  }

  get clicked(): ISignal<ToggleButton, boolean> {
    return this._clicked;
  }

  on_cls:string;
  off_cls: string;
  state: boolean;

  _clicked = new Signal<ToggleButton, boolean>(this);
}

class PanelItem extends Widget {
  constructor(options?:any) {
    super(options);
    this.addClass(PANEL_ITEM_CLASS);
    this._header = new Panel();
    this._header.addClass(PANEL_ITEM_HEADER_CLASS);

    this.set_toolbar();

    this._content = new Panel();
    this._content.addClass(PANEL_ITEM_CONTENTS_CLASS);

    let layout = new PanelLayout();
    this.layout = layout;
    layout.addWidget(this._header);
    layout.addWidget(this._content);
    if (options.widget) {
      this.widget = options.widget;
    }
    this._show();
  }

  set_toolbar() {
    this._title = new Button({cls: 'sp-item-title'});
    this._header.addWidget(this._title);

    let spacer = new Widget();
    spacer.addClass('sp-item-spacer');
    this._header.addWidget(spacer);

    this._maxButton = new ToggleButton({
      cls: 'sp-item-max',
      on: 'fa fa-window-minimize',
      off:'fa fa-window-maximize'
    });
    this._maxButton.clicked.connect(this.toggle, this);
    this._header.addWidget(this._maxButton);

    this._expandButton = new ToggleButton({
      cls: 'sp-item-expand',
      on: 'fa fa-compress',
      off: 'fa fa-expand'
    });
    this._expandButton.clicked.connect(this.on_expand, this);
    this._header.addWidget(this._expandButton);

    this._removeButton = new Button({cls: 'sp-item-remove fa fa-close'});
    this._removeButton.node.onclick = e => this.on_remove();
    this._header.addWidget(this._removeButton);

     this._title.node.onclick = e => this._maxButton.toggle();
  }

  dispose() {
    if (this.isDisposed) {
      return;
    }
    super.dispose();
    this._header = null;
    this._widget = null;
    this._content = null;
    this._title = null;
    this._removeButton = null;
    this._expandButton = null;
  }

  get widget() {
    return this._widget;
  }

  set widget(widget: Widget) {
    let oldWidget = this._widget;
    if (oldWidget) {
      oldWidget.disposed.disconnect(this._onChildDisposed, this);
      oldWidget.title.changed.disconnect(this._onTitleChanged, this);
      oldWidget.parent = null;
    }
    this._widget = widget;
    widget.disposed.connect(this._onChildDisposed, this);
    widget.title.changed.connect(this._onTitleChanged, this);
    this._onTitleChanged(widget.title);
    this._content.addWidget(widget);
  }

  get collapsed() {
    return this._collapsed;
  }

  set collapsed(value: boolean) {
    if (value === this._collapsed) {
      return;
    }
    if (value)
      this._hide();
    else
      this._show();
  }

  toggle() {
    this.collapsed = !this.collapsed;
  }

  get collapseChanged(): ISignal<PanelItem, void> {
    return this._collapseChanged;
  }

  on_expand() {
    this.expand(!this._expand);
  }

  expand(value:boolean) {
    this._expand = value;
    if (this._expand)
      this.addClass(PANEL_ITEM_CLASS_EXPAND);
    else
      this.removeClass(PANEL_ITEM_CLASS_EXPAND);

     this._expandChanged.emit(void 0);
  }

  on_remove() {
    console.log('remove');
    this._removeRequest.emit(void 0);
  }

  private _hide() {
    this._collapsed = true;
    if (this._content) {
      this._content.hide();
    }
    this.removeClass(PANEL_ITEM_CLASS_OPEN);
    this.removeClass( PANEL_ITEM_CLASS_EXPAND);
    this._collapseChanged.emit(void 0);
    this._expandButton.disable();
  }

  private _show() {
    this._collapsed = false;
    if (this._content) {
      this._content.show();
    }
    this.addClass(PANEL_ITEM_CLASS_OPEN);
    if (this._expand)
      this.addClass(PANEL_ITEM_CLASS_EXPAND);
    this._collapseChanged.emit(void 0);
    this._expandButton.enable();
  }

  get removeRequest(): ISignal<PanelItem, void> {
    return this._removeRequest;
  }

  get expandChanged(): ISignal<PanelItem, void> {
    return this._expandChanged;
  }


  /**
   * Handle the `changed` signal of a title object.
   */
  private _onTitleChanged(sender: Title<Widget>): void {
    this._title.node.textContent = this._widget.title.label;
  }

  private _onChildDisposed(sender: Widget): void {
    this.dispose();
  }

  _collapsed: boolean;
  _expand: boolean;
  _content: Panel;
  _widget: Widget;
  _header: Panel;
  _title: Button;
  _maxButton: ToggleButton;
  _expandButton: ToggleButton;
  _removeButton: Button;
   private _removeRequest = new Signal<PanelItem, void>(this);
   private _collapseChanged = new Signal<PanelItem, void>(this);
   private _expandChanged = new Signal<PanelItem, void>(this);
}


const SIDEPANEL_CLASS = 'sp-panel';

const SIDEPANEL_CHILD_CLASS = 'sp-panel-child';

export
class SidePanel extends Panel {
  constructor(options?: any) {
    super(options);
    this.addClass(SIDEPANEL_CLASS);
  }

  get removeRequest() :ISignal<SidePanel, number> {
    return this._removeRequest;
  }

  get itemWidgets(): ReadonlyArray<PanelItem> {
    return (this.layout as PanelLayout).widgets as ReadonlyArray<PanelItem>;
  }

  indexOf(widget: Widget): number {
    return ArrayExt.findFirstIndex(this.itemWidgets, (w: PanelItem) => w.widget === widget);
  }

  addWidget(widget: Widget): Widget {
    let collapse = this._wrapWidget(widget);
    super.addWidget(collapse);
    return collapse;
  }

  insertWidget(index: number, widget: Widget): void {
    let collapse = this._wrapWidget(widget);
    super.insertWidget(index, collapse);
  }

  removeWidget(widget: Widget): void {
    let index = this.indexOf(widget);
    if (index >= 0) {
      let item = this.itemWidgets[index] as PanelItem;
      item.parent = null;
      item.dispose();
    }
  }


  private _wrapWidget(widget: Widget) {
    let wrapped = new PanelItem({ widget });
    wrapped.addClass(SIDEPANEL_CHILD_CLASS);
    wrapped.collapseChanged.connect(this._onCollapseChange, this);
    wrapped.removeRequest.connect(this._onRemoveRequest, this);
    wrapped.expandChanged.connect(this._onExpandChange, this);
    return wrapped;
  }

  private _onCollapseChange(sender: PanelItem) {
    super.processMessage(Widget.ResizeMessage.UnknownSize);
    // console.log('collapse', sender);
    // if (!sender.collapsed) {
    //   this._selection.value = sender;
    // } else if (this._selection.value === sender && sender.collapsed) {
    //   this._selection.value = null;
    // }
  }

  private _onRemoveRequest(sender: PanelItem) {
    this._removeRequest.emit(this.indexOf(sender.widget));
    // this.removeWidget(sender.widget);
  }

  private _onExpandChange(sender:PanelItem) {
      super.processMessage(Widget.ResizeMessage.UnknownSize);
  }

  private _removeRequest = new Signal<SidePanel, number>(this);
}
