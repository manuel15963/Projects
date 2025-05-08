import { Routes } from '@angular/router';
import { MainLayoutComponent } from './layout/main-layout.component';
import { ListComponent } from './feature/products/listar/list.component';
import { CreateComponent } from './feature/products/form-crear/create.component';

export const routes: Routes = [
  {
    path: '',
    component: MainLayoutComponent,
    children: [
      { path: '', redirectTo: 'products', pathMatch: 'full' },  // redirección por defecto
      { path: 'products', component: ListComponent },
      { path: 'products/create', component: CreateComponent }
    ]
  }
];
