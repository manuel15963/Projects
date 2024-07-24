import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from "@angular/material/dialog";
import { BooksService } from "../books.service";
import { Books } from "../model/books.model";
import { BooksFormComponent } from "../books-form/books-form.component";
import localeEs from '@angular/common/locales/es';
import { registerLocaleData } from '@angular/common';
import { DatePipe } from '@angular/common';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';

// Registra la configuración regional para español
registerLocaleData(localeEs);

@Component({
  selector: 'app-books-list',
  templateUrl: './books-list.component.html',
  styleUrls: ['./books-list.component.scss'],
  providers: [DatePipe]
})
export class BooksListComponent implements OnInit {

  displayedColumns: string[] = ['title', 'author', 'isbn', 'publisher', 'publisheddate', 'pages', 'language', 'description', 'action'];
  dataSource = new MatTableDataSource<Books>([]);
  estadoFiltrado: string = 'Todos';
  titleFiltrado: string = '';
  languageFiltrado: string = '';
  selectedDate: Date | null = null;

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(public dialog: MatDialog, private booksService: BooksService, private datePipe: DatePipe) { }

  ngOnInit(): void {
    this.listar();
  }

  listar() {
    this.booksService.getBooks().subscribe((res: Books[]) => {
      console.log('Datos recibidos:', res);
      this.dataSource.data = res.filter(book => {
        const matchesEstado = this.estadoFiltrado === 'Todos' || book.status === this.estadoFiltrado;
        const matchesTitle = this.titleFiltrado === '' || book.title.toLowerCase().includes(this.titleFiltrado.toLowerCase());
        const matchesLanguage = this.languageFiltrado === '' || book.language.toLowerCase().includes(this.languageFiltrado.toLowerCase());
        const matchesDate = this.applyDateFilter(book.publisheddate);
        console.log(`Libro: ${book.title}, Fecha: ${book.publisheddate}, Coincide con la fecha: ${matchesDate}`);
        return matchesEstado && matchesTitle && matchesLanguage && matchesDate;
      });
      this.dataSource.paginator = this.paginator;
      console.log('Datos filtrados:', this.dataSource.data);
    });
  }

  applyDateFilter(publishedDate: string): boolean {
    if (this.selectedDate) {
      const selectedDateStart = this.toStartOfDay(this.selectedDate);
      const selectedDateEnd = this.toEndOfDay(this.selectedDate);
      const publishedDateObj = new Date(publishedDate);
      const publishedDateStart = this.toStartOfDay(publishedDateObj);

      console.log(`Comparando: ${publishedDateStart.toISOString()} con ${selectedDateStart.toISOString()} y ${selectedDateEnd.toISOString()}`);

      return publishedDateStart >= selectedDateStart && publishedDateStart <= selectedDateEnd;
    }
    return true;
  }

  toStartOfDay(date: Date): Date {
    return new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()));
  }

  toEndOfDay(date: Date): Date {
    return new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(), 23, 59, 59, 999));
  }

  openDialog(): void {
    this.booksService.booksSelected = undefined;
    const dialogRef = this.dialog.open(BooksFormComponent, {
      width: '35%',
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.dataSource.data.unshift(result);
      }
      this.listar();
    });
  }

  editarBooks(books: Books) {
    this.booksService.booksSelected = books;
    const dialogRef = this.dialog.open(BooksFormComponent, {
      width: '35%',
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        const index = this.dataSource.data.findIndex(u => u.id === result.id);
        if (index !== -1) {
          this.dataSource.data[index] = result;
        }
      }
      this.listar();
    });
  }

  deleteBooks(id: number | undefined): void {
    if (id !== undefined) {
      this.booksService.deleteBooks(id).subscribe(() => {
        console.log('Libro eliminado correctamente');
        this.listar();
      }, error => {
        console.error('Error al eliminar el libro:', error);
      });
    }
  }

  activarBooks(id: number | undefined): void {
    if (id !== undefined) {
      this.booksService.restoreBooks(id).subscribe({
        next: () => {
          console.log('Libro activado correctamente.');
          this.listar();
        },
        error: (err) => {
          console.error('Error al activar el libro:', err);
        }
      });
    }
  }

  clearFilters(): void {
    this.titleFiltrado = '';
    this.languageFiltrado = '';
    this.selectedDate = null;
    this.listar();  // Volver a listar los libros con los filtros limpios
  }
}
