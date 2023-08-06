// Copyright (c) Alexey Strokach
// Distributed under the terms of the Modified BSD License.

import { DOMWidgetModel, DOMWidgetView, ISerializers } from "@jupyter-widgets/base";
import * as MSA from "msa";
import "../css/msa.css";
import "../css/widget.css";
import { MODULE_NAME, MODULE_VERSION } from "./version";

export class MSAModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: MSAModel.model_name,
      _model_module: MSAModel.model_module,
      _model_module_version: MSAModel.model_module_version,
      _view_name: MSAModel.view_name,
      _view_module: MSAModel.view_module,
      _view_module_version: MSAModel.view_module_version
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers
    // Add any extra serializers here
  };

  static model_name = "MSAModel";
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = "MSAView"; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class MSAView extends DOMWidgetView {
  render() {
    this.el.classList.add("jp-RenderedMSA");
    let msaDiv = document.createElement("div");
    this.msa = new MSA.msa({
      el: msaDiv,
      vis: {
        labelId: false,
        sequences: true,
        markers: true,
        metacell: false,
        conserv: false,
        overviewbox: false,
        seqlogo: true,
        gapHeader: false,
        leftHeader: true
      }
    });
    this.el.appendChild(msaDiv);

    this.model.on("change:value", this.value_changed.bind(this), this);

    // this.model.on("msg:custom", this.on_msg, this);
  }

  value_changed() {
    let seqs = this.model.get("value");
    // console.log("seqs:", seqs);
    // let seqs = MSA.io.fasta.parse(data);
    // if (this.msa.seqs.length > 100) {
    //   this.msa.seqs.pop();
    // }
    this.msa.seqs.reset(seqs);
    this.msa.render();
  }

  on_msg(msg: any) {
    console.log("msg.type", msg.type);
    console.log("msg.target", msg.target);
    console.log("msg.methodName", msg.methodName);
    console.log("msg.args", msg.args);
    console.log("msg.kwargs", msg.kwargs);

    console.assert(msg.type === "call_method");

    let new_args = msg.args.slice();
    new_args.push(msg.kwargs);

    let target: any;
    switch (msg.target) {
      case "MSA":
        target = this.msa;
      case "SEQS":
        target = this.msa.seqs;
      // *reset*
      // this.msa.seqs.reset(seqs);
      // *add*

      default:
        console.warn("There is no method for " + msg.target);
        break;
    }
    let func = target[msg.methodName];
    func.apply(target, new_args);
    // this.msa.render();
  }

  msa: any;
}
