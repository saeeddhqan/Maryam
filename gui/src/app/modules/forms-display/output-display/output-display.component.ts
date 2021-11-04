import { Component, Input, OnInit } from '@angular/core';
import { module_meta } from 'src/app/common-resources/modules-meta';
import { ApiRequestService } from '../api-request.service';

@Component({
  selector: 'app-output-display',
  templateUrl: './output-display.component.html',
  styleUrls: ['./output-display.component.css']
})
export class OutputDisplayComponent implements OnInit {
  
  @Input() final_arg_list: string[];
  @Input() flag: boolean;
  display_string: any[];
  command_string: string = ""
  test: string
  constructor(private service:ApiRequestService) { }

  ngOnInit(): void {
    /*
    this.command_string = ''
    this.test = 'test'
    if (this.flag == true) {
      this.test = 'Nani the fuck?'
    }
    if (this.flag == true) {
      for (let index = 0; index < this.final_arg_list.length; index++) {
        this.command_string = this.command_string + this.final_arg_list[index];
        
      }
      this.service.runCmd(this.command_string).subscribe(data=>{
        this.display_string = data
        this.test = 'inside runCMD'
      })      
    }
    */
  }

}
