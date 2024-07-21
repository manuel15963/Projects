import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DemoFlexyModule } from '../demo-flexy-module'
import { DashboardComponent } from './dashboard.component';
import { CardsComponent } from './dashboard-components/cards/cards.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { NgApexchartsModule } from 'ng-apexcharts';

@NgModule({
  declarations: [
    DashboardComponent,
    CardsComponent,
  ],
    imports: [
        CommonModule,
        DemoFlexyModule,
        FormsModule,
        NgApexchartsModule,
        ReactiveFormsModule
    ],
  exports: [
    DashboardComponent,
  ]
})
export class DashboardModule { }
