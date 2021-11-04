import { Component, OnInit } from '@angular/core';
import { Form, FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { module_meta } from 'src/app/common-resources/modules-meta';
import { ApiRequestService } from './api-request.service';

@Component({
  selector: 'app-forms-display',
  templateUrl: './forms-display.component.html',
  styleUrls: ['./forms-display.component.css']
})
export class FormsDisplayComponent implements OnInit {

  flag: boolean = false
  module_meta = module_meta
  
  loaded_module: string = this.route.snapshot.params['modulename']

  params: any[] = module_meta[this.loaded_module]['options']
  params_length: number = this.params.length
  constructor(private route: ActivatedRoute, private service:ApiRequestService) { }

  module_input_form: FormGroup;
  form_data: [any, any, String][] ;
  args_html_list: [number, string, string][] = [
    [0, 'arg0', 'arg0_button'], 
    [1, 'arg1', 'arg1_button'],
    [2, 'arg2', 'arg2_button'], 
    [3, 'arg3', 'arg3_button'], 
    [4 ,'arg4', 'arg4_button'], 
    [5, 'arg5', 'arg5_button'], 
    [6, 'arg6', 'arg6_button'], 
    [7, 'arg7', 'arg7_button'], 
    [8, 'arg8', 'arg8_button'], 
    [9, 'arg9', 'arg9_button']
  ]

  ngOnInit(): void { 
    this.module_input_form = new FormGroup({
      "arg0": new FormControl(0 < this.params_length ? this.params[0][1] : null),
      "arg0_button": new FormControl(0 < this.params_length ? this.params[0][1] : null),
      "arg1": new FormControl(1 < this.params_length ? this.params[1][1] : null),
      "arg1_button": new FormControl(1 < this.params_length ? this.params[1][1] : null),
      "arg2": new FormControl(2 < this.params_length ? this.params[2][1] : null),
      "arg2_button": new FormControl(2 < this.params_length ? this.params[2][1] : null),
      "arg3": new FormControl(3 < this.params_length ? this.params[3][1] : null),
      "arg3_button": new FormControl(3 < this.params_length ? this.params[3][1] : null),
      "arg4": new FormControl(4 < this.params_length ? this.params[4][1] : null),
      "arg4_button": new FormControl(4 < this.params_length ? this.params[4][1] : null),
      "arg5": new FormControl(5 < this.params_length ? this.params[5][1] : null),
      "arg5_button": new FormControl(5 < this.params_length ? this.params[5][1] : null),
      "arg6": new FormControl(6 < this.params_length ? this.params[6][1] : null),
      "arg6_button": new FormControl(6 < this.params_length ? this.params[6][1] : null),
      "arg7": new FormControl(7 < this.params_length ? this.params[7][1] : null),
      "arg7_button": new FormControl(7 < this.params_length ? this.params[7][1] : null),
      "arg8": new FormControl(8 < this.params_length ? this.params[8][1] : null),
      "arg8_button": new FormControl(8 < this.params_length ? this.params[8][1] : null),
      "arg9": new FormControl(9 < this.params_length ? this.params[9][1] : null),
      "arg9_button": new FormControl(9 < this.params_length ? this.params[9][1] : null),
    })
  }

  temp: any;
  args_list: string[];
  command_string: string;
  display_string: any[];
  test: string;
  command_set: { [meta: string]: string }
  onSubmit() {
    this.flag = true
    this.form_data = []
    this.args_list = []
    this.command_string = ''
    this.display_string = []
    this.test = ''
    for (let index = 0; index < this.args_html_list.length; index++) {
      if (this.module_input_form.value[this.args_html_list[index][1]] != this.module_input_form.value[this.args_html_list[index][2]]){
        if (this.module_input_form.value[this.args_html_list[index][1]] != this.params[index][2] ) {
          this.args_list.push(this.params[index][4])
          if (
            this.module_input_form.value[this.args_html_list[index][2]] != 'true' && 
            this.module_input_form.value[this.args_html_list[index][2]] != 'false') {
            this.args_list.push(this.module_input_form.value[this.args_html_list[index][1]])
          }
        }
        if (this.module_input_form.value[this.args_html_list[index][2]] != this.params[index][2].toString()) {
          if (this.args_list.indexOf(this.params[index][4]) == -1) {
            this.args_list.push(this.params[index][4])
          }
        }
      } 
    }

    for (let index = 0; index < this.args_list.length; index++) {
      this.command_string = this.command_string + " " + this.args_list[index];
    }
    this.command_set = {
      "modulename": this.loaded_module,
      "command": this.command_string
    }
    this.service.runCmd(this.command_set).subscribe(data=>{
      this.display_string = data
    }) 
  }
}
