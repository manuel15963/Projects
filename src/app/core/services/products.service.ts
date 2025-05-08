import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { product } from '../interfaces/product';

@Injectable({
  providedIn: 'root'
})
export class ProductsService {
  private apiUrl = 'http://localhost:8085/api/products';

  constructor(private http: HttpClient) {}

  getAll(): Observable<product[]> {
    return this.http.get<product[]>(this.apiUrl);
  }

  getById(id: number): Observable<product> {
    return this.http.get<product>(`${this.apiUrl}/${id}`);
  }

  create(product: product): Observable<product> {
    return this.http.post<product>(this.apiUrl, product);
  }

  update(id: number, product: product): Observable<product> {
    return this.http.put<product>(`${this.apiUrl}/${id}`, product);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
