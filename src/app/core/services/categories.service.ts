import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { category } from '../interfaces/category';

@Injectable({
  providedIn: 'root'
})
export class CategoriesService {
  private apiUrl = 'http://localhost:8085/api/categories';

  constructor(private http: HttpClient) {}

  getAll(): Observable<category[]> {
    return this.http.get<category[]>(this.apiUrl);
  }
  

  getById(id: number): Observable<category> {
    return this.http.get<category>(`${this.apiUrl}/${id}`);
  }

  create(category: category): Observable<category> {
    return this.http.post<category>(this.apiUrl, category);
  }

  update(id: number, category: category): Observable<category> {
    return this.http.put<category>(`${this.apiUrl}/${id}`, category);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
