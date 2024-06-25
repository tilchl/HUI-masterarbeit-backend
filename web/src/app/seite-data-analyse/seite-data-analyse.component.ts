import { Component, ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-seite-data-analyse',
  templateUrl: './seite-data-analyse.component.html',
  styleUrls: ['./seite-data-analyse.component.css']
})
export class SeiteDataAnalyseComponent {
  listItems: { [ket: string]: ("Experiment" | "PreData" | "PostData" | "CPA" | "Process")[] } = {
    "analyse of": ["Experiment", "PreData", "PostData", "CPA", "Process"]
  }

  which: ("Experiment" | "PreData" | "PostData" | "CPA" | "Process")[] = []
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
    // if (this.history != value) {
    //   this.which = [value]
    // }
    this.which = [value]
  }
}
