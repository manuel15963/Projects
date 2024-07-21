import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { MatDialogRef } from "@angular/material/dialog";
import { UsersService } from "../service/users-service.service";
import Swal from "sweetalert2";

@Component({
  selector: 'app-users-form',
  templateUrl: './users-form.component.html',
  styleUrls: ['./users-form.component.scss']
})
export class UsersFormComponent implements OnInit, OnDestroy {
  userForm: FormGroup = new FormGroup({});
  isEditMode = false;

  constructor(
    public dialogRef: MatDialogRef<UsersFormComponent>,
    private fb: FormBuilder,
    public usersService: UsersService
  ) { }

  ngOnDestroy(): void {
    // Limpieza de recursos o subscripciones si es necesario
  }

  ngOnInit(): void {
    this.initUserForm();
  }

  initUserForm() {
    this.userForm = this.fb.group({
      id: [null],
      username: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      firstname: ['', [Validators.required]],
      lastname: ['', [Validators.required]],
      birthdate: [{ value: '', disabled: this.isEditMode }, [Validators.required]],
      phone: ['', [Validators.required]],
      role: ['', [Validators.required]],
      password: [''],
      status: ['A'],
    });

    if (this.usersService.userSelected) {
      this.isEditMode = true;
      this.userForm.patchValue(this.usersService.userSelected);
      this.userForm.get('password')?.clearValidators();
      this.userForm.get('password')?.updateValueAndValidity();
      this.userForm.get('birthdate')?.disable();
      this.userForm.get('password')?.disable();
    }
  }

  saveEntidades() {
    if (this.isEditMode) {
      this.updateUsers();
    } else {
      this.createUser();
    }
  }

  createUser() {
    const newUser = { ...this.userForm.getRawValue(), status: 'A' };
    this.usersService.addUser(newUser).subscribe(res => {
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

  updateUsers() {
    if (this.usersService.userSelected) {
      const id = this.usersService.userSelected.id;
      const updatedUser = { ...this.userForm.getRawValue(), birthdate: this.usersService.userSelected.birthdate };
      this.usersService.updateUser(id, updatedUser).subscribe(res => {
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
