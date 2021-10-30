import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ModulesComponent } from './modules/modules.component';
import { FormsDisplayComponent } from './modules/forms-display/forms-display.component';
import { OutputDisplayComponent } from './modules/forms-display/output-display/output-display.component';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    ModulesComponent,
    FormsDisplayComponent,
    OutputDisplayComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
