import { ChangeDetectorRef, Component } from '@angular/core';

@Component({
  selector: 'app-seite-data-storage',
  templateUrl: './seite-data-storage.component.html',
  styleUrls: ['./seite-data-storage.component.css']
})
export class SeiteDataStorageComponent {
  listItems: { [ket: string]: ("Experiment" | "PreData" | "PostData" | "CPA" | "Process")[] } = {
    "uploader for": ["Experiment", "PreData", "PostData", "CPA", "Process"]
  }
  which: ("Experiment" | "PreData" | "PostData" | "CPA" | "Process")[] = ['Experiment']
  history: any = ''

  constructor(private cdref: ChangeDetectorRef) { }
  
  getObjectKeys(obj: any): string[] {
    return Object.keys(obj);
  }

  isSelected(value: string): boolean {
    return value === this.which[0];
  }

  ngAfterContentChecked() {
    this.cdref.detectChanges();
  }

  setWhich(value: "Experiment" | "PreData" | "PostData" | "CPA" | "Process") {
    this.history = this.which
    if (this.history != value) {
      this.which = [value]
    }
  }
}
