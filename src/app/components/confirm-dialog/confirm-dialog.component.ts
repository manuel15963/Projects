import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-confirm-dialog',
  templateUrl: './confirm-dialog.component.html',
  styleUrls: ['./confirm-dialog.component.scss']
})
export class ConfirmDialogComponent {

  data: any;
  dni: string | undefined;

  constructor(public dialogRef: MatDialogRef<ConfirmDialogComponent>) {}

  onNo(): void {
    this.dialogRef.close(false);
  }

  onYes(): void {
    this.dialogRef.close(true);
  }
}
