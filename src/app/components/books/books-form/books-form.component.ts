import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { BooksService } from '../books.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-books-form',
  templateUrl: './books-form.component.html',
  styleUrls: ['./books-form.component.scss']
})
export class BooksFormComponent implements OnInit, OnDestroy {
  booksForm: FormGroup;
  isEditMode: boolean = false;

  constructor(
    public dialogRef: MatDialogRef<BooksFormComponent>,
    private fb: FormBuilder,
    public booksService: BooksService
  ) {
    this.booksForm = this.fb.group({
      id: [null],
      title: ['', [Validators.required, Validators.pattern(/^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s]+$/)]],
      author: ['', [Validators.required, Validators.pattern(/^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s]+$/)]],
      isbn: ['', [Validators.required, Validators.pattern(/^\d{13}$/)]],
      publisher: ['', [Validators.required, Validators.pattern(/^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s]+$/)]],
      publisheddate: [{ value: '', disabled: this.isEditMode }, [Validators.required]],
      pages: ['', [Validators.required, Validators.pattern(/^\d{1,4}$/)]],
      language: ['', [Validators.required, Validators.pattern(/^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+$/)]],
      description: ['', [Validators.required, Validators.pattern(/^[a-zA-Z0-9áéíóúüñÁÉÍÓÚÜÑ\s]{1,200}$/)]],
      status: ['A']
    });
  }

  ngOnDestroy(): void {
    this.booksService.booksSelected = undefined;
  }

  ngOnInit(): void {
    if (this.booksService.booksSelected) {
      this.isEditMode = true;
      this.booksForm.patchValue(this.booksService.booksSelected);
    }
  }

  saveBooks() {
    if (this.booksForm.invalid) {
      return; // Evita guardar si el formulario es inválido
    }

    if (this.isEditMode) {
      this.updateBooks();
    } else {
      this.createBooks();
    }
  }

  createBooks() {
    const newBooks = { ...this.booksForm.getRawValue(), status: 'A' };
    this.booksService.addBooks(newBooks).subscribe(res => {
      Swal.fire({
        position: 'top-end',
        icon: 'success',
        title: 'Registro completado con éxito',
        showConfirmButton: false,
        timer: 3000,
        toast: true,
        background: '#40c2d3',
        color: '#ffffff',
        customClass: {
          popup: 'custom-toast'
        }
      });
      this.dialogRef.close(res); // Devolver el usuario creado
    });
  }

  updateBooks() {
    if (this.booksService.booksSelected) {
      const id = this.booksService.booksSelected.id;
      const updatedBooks = {
        ...this.booksForm.getRawValue(),
        publisheddate: this.booksService.booksSelected.publisheddate
      };
      this.booksService.updateBooks(id, updatedBooks).subscribe(res => {
        this.dialogRef.close(res); // Devolver el usuario actualizado
      });
    } else {
      console.error('No se ha seleccionado ningún usuario para actualizar.');
    }
  }

  onClose(): void {
    this.dialogRef.close();
  }
}
