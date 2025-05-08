// create.component.ts
import { Component, inject, OnInit } from '@angular/core';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { Observable, of, map, startWith } from 'rxjs';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialogRef } from '@angular/material/dialog';
import { MatAutocompleteModule } from '@angular/material/autocomplete';

import { ProductsService } from '@core/services/products.service';
import { product } from '@core/interfaces/product';
import { CategoriesService } from '@core/services/categories.service';

@Component({
  selector   : 'app-create-product',
  standalone : true,
  templateUrl: './create.component.html',
  styleUrls  : ['./create.component.scss'],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatAutocompleteModule
  ]
})
export class CreateComponent implements OnInit {
  // ────────────────────────────────── inyecciones
  private dialogRef   = inject(MatDialogRef<CreateComponent>);
  private productsSrv = inject(ProductsService);
  private snackBar    = inject(MatSnackBar);
  private categories  = inject(CategoriesService);

  // ────────────────────────────────── modelo
  product: product = {
    name          : '',
    description   : '',
    unitPrice     : 0,
    stocks        : 0,
    expirationDate: '',
    status        : '1',
    category      : { id: 0, name: '' }
  };

  // ────────────────────────────────── autocomplete
  categoryControl      = new FormControl('');
  filteredCategories$: Observable<string[]> = of([]);
  allCategories: string[] = [];

  ngOnInit(): void {
    this.categories.getAll().subscribe(data => {
      this.allCategories = data.map(c => c.name);
      this.filteredCategories$ = this.categoryControl.valueChanges.pipe(
        startWith(''),
        map(value => this._filter(this.normalizeText(value ?? '')))
      );
    });
  }

  /* Convierte a minúsculas, elimina tildes y espacios extra */
  private normalizeText(text: string): string {
    return text
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')   // quita diacríticos
      .trim();
  }

  /* Devuelve coincidencias según lo escrito */
  private _filter(value: string): string[] {
    return this.allCategories.filter(option =>
      this.normalizeText(option).includes(value)
    );
  }

  onCategorySelected(name: string): void {
    this.product.category.name = name;           // asigna la seleccionada
  }

  // ────────────────────────────────── guardar
  submit(): void {
    const categoryName = (this.categoryControl.value ?? '').trim();
    if (!categoryName) {
      this.snackBar.open('Debe ingresar una categoría válida', 'Cerrar');
      return;
    }

    // asignamos la categoría escrita o seleccionada
    this.product.category.name = categoryName;

    // limpiamos ids = 0 para evitar conflictos en el backend
    if ((this.product as any).id === 0)            delete (this.product as any).id;
    if (this.product.category.id === 0)            delete  this.product.category.id;

    this.productsSrv.create(this.product).subscribe({
      next : ()   => { this.snackBar.open('Producto creado', 'OK', { duration: 2500 }); this.dialogRef.close(true);  },
      error: ()   =>   this.snackBar.open('Error al crear', 'Cerrar')
    });
  }
}
