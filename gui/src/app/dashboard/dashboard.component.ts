import { Component, Injectable, OnInit } from '@angular/core';
import { module_meta } from '../common-resources/modules-meta';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})

export class DashboardComponent implements OnInit {

  constructor() { }
  meta = module_meta
  ngOnInit(): void {
  }

}
