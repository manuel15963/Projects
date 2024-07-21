import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FeatherModule } from 'angular-feather';
import { allIcons } from 'angular-feather/icons';
import { DemoFlexyModule } from '../demo-flexy-module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ConfirmDialogComponent } from './confirm-dialog/confirm-dialog.component';
import { UsersListComponent } from './users/users-list/users-list.component';
import { UsersFormComponent } from './users/users-form/users-form.component';
import { NzCardModule } from "ng-zorro-antd/card";
import { NzSelectModule } from "ng-zorro-antd/select";
import { NzTableModule } from "ng-zorro-antd/table";
import { NzModalModule } from "ng-zorro-antd/modal";

@NgModule({
  imports: [
    CommonModule,
    FeatherModule.pick(allIcons),
    DemoFlexyModule,
    FormsModule,
    ReactiveFormsModule,
    NzCardModule,
    NzSelectModule,
    NzTableModule,
    NzModalModule,
  ],
  declarations: [
    ConfirmDialogComponent,
    UsersListComponent,
    UsersFormComponent,
  ]
})
export class ComponentsModule { }
