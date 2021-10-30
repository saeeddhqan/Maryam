import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { module_meta } from '../common-resources/modules-meta';

@Component({
  selector: 'app-modules',
  templateUrl: './modules.component.html',
  styleUrls: ['./modules.component.css']
})
export class ModulesComponent implements OnInit {
  loaded_module: string = '';
  keys: string[] = [''];
  constructor(private route: ActivatedRoute) { }
  
  ngOnInit(): void {
    this.loaded_module = this.route.snapshot.params['modulename']
    this.keys = Object.keys(module_meta)
  }

}
