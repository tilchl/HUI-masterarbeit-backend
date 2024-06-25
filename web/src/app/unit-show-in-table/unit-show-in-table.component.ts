import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-unit-show-in-table',
  templateUrl: './unit-show-in-table.component.html',
  styleUrls: ['./unit-show-in-table.component.css']
})
export class UnitShowInTableComponent implements OnChanges {
  @Input() textareaContent!: string

  headers: string[] = [];
  dataRows: string[][] = [];

  ngOnChanges(changes: SimpleChanges): void {
    this.headers = []
    this.dataRows = []
    this.parseContent();
  }

  parseContent() {
    if (this.textareaContent) {
      const lines = this.textareaContent.split('\n');
      this.headers = lines[0].split(';').map(header => header.trim());
      for (let i = 1; i < lines.length; i++) {
        const cells = lines[i].split(';').map(cell => cell.trim());
        this.dataRows.push(cells);
      }
    }
  }
}
