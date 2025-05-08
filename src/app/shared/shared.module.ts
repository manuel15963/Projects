import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

/* Material */
import { MatTableModule }   from '@angular/material/table';
import { MatButtonModule }  from '@angular/material/button';
import { MatCardModule }    from '@angular/material/card';
import { MatIconModule }    from '@angular/material/icon';
import { MatSnackBarModule } from '@angular/material/snack-bar';

@NgModule({
  imports : [
    CommonModule,
    MatTableModule,
    MatButtonModule,
    MatCardModule,
    MatIconModule,
    MatSnackBarModule
  ],
  exports : [
    MatTableModule,
    MatButtonModule,
    MatCardModule,
    MatIconModule,
    MatSnackBarModule
  ]
})
export class SharedModule {}
