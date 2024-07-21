import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FullComponent } from './layouts/full/full.component';
import {UsersListComponent} from "./components/users/users-list/users-list.component";

const routes: Routes = [
  {
    path:"",
    component:FullComponent,
    children: [
      {path:"users", component:UsersListComponent},
    ]
  },

  {path:"", redirectTo:"/home", pathMatch:"full"},
  {path:"**", redirectTo:"/home", pathMatch:"full"},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
