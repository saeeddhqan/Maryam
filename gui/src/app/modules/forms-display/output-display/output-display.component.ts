import { Component, Input, OnInit } from '@angular/core';
import { module_meta } from 'src/app/common-resources/modules-meta';

@Component({
  selector: 'app-output-display',
  templateUrl: './output-display.component.html',
  styleUrls: ['./output-display.component.css']
})
export class OutputDisplayComponent implements OnInit {
  
  @Input() form_input_data: [any, any, String][];
  final_arg_list: string[];

  constructor() { }

  ngOnInit(): void {
    for (let element in this.form_input_data) {
      if (typeof(element)=='boolean') {

        
      }
      
    }
  }

}
