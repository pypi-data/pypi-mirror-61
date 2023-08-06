import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

import { SidePanelView, SidePanelModel } from './widget_sidepanel';
import { SideOutput, SideOutputModel } from './SideOutput';

import { EXTENSION_SPEC_VERSION } from './version';

const EXTENSION_ID = 'sidepanel';


function activate(app: JupyterFrontEnd, registry: IJupyterWidgetRegistry): void {
  let AppSideOutput = class extends SideOutput {
    constructor(options: any) {
      super({app, ...options});
    }
  };

  let AppSidePanel = class extends SidePanelView {
    constructor(options: any) {
      super({app, ...options});
    }
  };

  registry.registerWidget({
    name: EXTENSION_ID,
    version: EXTENSION_SPEC_VERSION,
    exports: {
      SideOutputModel: SideOutputModel,
      SideOutput: AppSideOutput,
      SidePanelModel: SidePanelModel,
      SidePanel: AppSidePanel,
    }
  });
}

const plugin: JupyterFrontEndPlugin<void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  activate: activate,
  autoStart: true
};

export default  plugin;
