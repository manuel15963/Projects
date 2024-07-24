import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable, switchMap} from "rxjs";
import {Books} from "./model/books.model";

@Injectable({
  providedIn: 'root'
})

export class BooksService {
  private apiUrl = 'http://localhost:8081/api/books';

  constructor(private http: HttpClient) {
  }

  booksSelected: Books | undefined;

  getBooks(): Observable<Books[]> {
    return this.http.get<Books[]>(this.apiUrl);
  }

  getBooksById(id: number): Observable<Books> {
    return this.http.get<Books>(`${this.apiUrl}/${id}`);
  }

  addBooks(books: Books): Observable<Books> {
    books.status = 'A';
    return this.http.post<Books>(this.apiUrl, books);
  }

  updateBooks(id: number | undefined, books: Books): Observable<Books> {
    return this.http.put<Books>(`${this.apiUrl}/${id}`, books);
  }

  deleteBooks(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  restoreBooks(id: number): Observable<Books> {
    return this.getBooksById(id).pipe(
      switchMap((books: Books) => {
        books.status = 'A';
        return this.updateBooks(id, books);
      })
    )
  }
}
