import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import {Observable, switchMap} from "rxjs";
import { User } from "../model/users.model";

@Injectable({
  providedIn: 'root'
})
export class UsersService {
  private apiUrl = 'http://localhost:8080/api/users';

  constructor(private http: HttpClient) {}
  userSelected: User | undefined;

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUrl);
  }

  getUserById(id: number): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/${id}`);
  }

  addUser(user: User): Observable<User> {
    user.status = 'A'; // Asignar estado activo por defecto
    return this.http.post<User>(`${this.apiUrl}/register`, user);
  }

  updateUser(id: number | undefined, user: User): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}/${id}`, user);
  }

  deleteUser(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  restoreUser(id: number): Observable<User> {
    return this.getUserById(id).pipe(
      switchMap((user: User) => {
        user.status = 'A';
        return this.updateUser(id, user);
      })
    );
  }
}
