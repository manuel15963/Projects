import { Component, OnInit } from '@angular/core';
import { User } from "../model/users.model";
import { MatDialog } from "@angular/material/dialog";
import { UsersService } from "../service/users-service.service";
import { UsersFormComponent } from "../users-form/users-form.component";

@Component({
  selector: 'app-users-list',
  templateUrl: './users-list.component.html',
  styleUrls: ['./users-list.component.scss']
})
export class UsersListComponent implements OnInit {

  dataSource: User[] = [];
  estadoFiltrado: string = 'Todos';

  constructor(public dialog: MatDialog, private usersService: UsersService) {}

  ngOnInit(): void {
    this.listar();
  }

  listar() {
    this.usersService.getUsers().subscribe((res: User[]) => {
      this.dataSource = this.estadoFiltrado === 'Todos' ? res : res.filter((user) => user.status === this.estadoFiltrado);
    });
  }

  openDialog(): void {
    this.usersService.userSelected = undefined; // Limpiar selección de usuario
    const dialogRef = this.dialog.open(UsersFormComponent, {
      width: '35%',
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.dataSource.unshift(result); // Insertar el nuevo usuario al inicio de la lista
      }
      this.listar();
    });
  }

  editarEntidad(user: User) {
    this.usersService.userSelected = user;
    const dialogRef = this.dialog.open(UsersFormComponent, {
      width: '35%',
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        const index = this.dataSource.findIndex(u => u.id === result.id);
        if (index !== -1) {
          this.dataSource[index] = result; // Actualizar el usuario en la lista
        }
      }
      this.listar();
    });
  }

  deleteUser(id: number | undefined): void {
    if (id !== undefined) {
      this.usersService.deleteUser(id).subscribe(() => {
        console.log('Usuario desactivado correctamente');
        this.listar();
      }, error => {
        console.error('Error al desactivar el usuario:', error);
      });
    }
  }

  activarEntidad(id: number | undefined): void {
    if (id !== undefined) {
      this.usersService.restoreUser(id).subscribe({
        next: () => {
          console.log('Usuario activado correctamente.');
          this.listar();
        },
        error: (err) => {
          console.error('Error al activar el usuario:', err);
        }
      });
    }
  }
}
