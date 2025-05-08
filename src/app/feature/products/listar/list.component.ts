/* src/app/feature/products/listar/list.component.ts */
import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatTableModule }  from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule }   from '@angular/material/icon';
import { MatDialog }       from '@angular/material/dialog';
import { MatSnackBar }     from '@angular/material/snack-bar';
import { MatCardModule }   from '@angular/material/card';

import { product }          from '@core/interfaces/product';
import { ProductsService }  from '@core/services/products.service';
import { CreateComponent }  from '@feature/products/form-crear/create.component';
import { MatDividerModule } from '@angular/material/divider';


@Component({
  selector  : 'app-product-list',
  standalone: true,
  templateUrl: './list.component.html',
  styleUrls : ['./list.component.scss'],
  imports: [
    CommonModule,
    MatCardModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatDividerModule 
  ]
})
export class ListComponent {

  displayedColumns = ['name','description','price','stock','date','category','state','actions'];
  products : product[] = [];
  isLoading = false;

  private srv    = inject(ProductsService);
  private dialog = inject(MatDialog);
  private snack  = inject(MatSnackBar);

  constructor() { this.load(); }

  load(): void {
    this.isLoading = true;
    this.srv.getAll().subscribe({
      next : d => { this.products = d; this.isLoading = false; },
      error: () => { this.snack.open('Error al cargar','Cerrar'); this.isLoading=false; }
    });
  }

  delete(id:number):void {
    this.srv.delete(id).subscribe({
      next : () => { this.snack.open('Eliminado','OK',{duration:2e3}); this.load(); },
      error: () => this.snack.open('Error al eliminar','Cerrar')
    });
  }

  /* diálogo de creación */
  openCreateDialog(): void {
    const ref = this.dialog.open(CreateComponent,{width:'600px'});
    ref.afterClosed().subscribe(ok => { if (ok) this.load(); });
  }
}
