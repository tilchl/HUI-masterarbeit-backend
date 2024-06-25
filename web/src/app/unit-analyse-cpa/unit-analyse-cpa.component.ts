import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { QueryNeo4jService } from '../app-services';
import { UnitEditDatabaseComponent } from '../unit-edit-database/unit-edit-database.component';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-unit-analyse-cpa',
  templateUrl: './unit-analyse-cpa.component.html',
  styleUrls: ['./unit-analyse-cpa.component.css']
})
export class UnitAnalyseCpaComponent {
  @Input() staticOrNot!: boolean
  @Input() openSearch!: { which: "Experiment" | "PreData" | "PostData" | "CPA" | "Process", selectedId: string[] }
  @Output() deleteOne: EventEmitter<string> = new EventEmitter<string>()

  callBacks: any[] = []

  showGraphController: string[] = []
  constructor(
    private queryNeo4jService: QueryNeo4jService,
    public dialog: MatDialog,
  ) { }

  searchOne(ID: readonly string[], data_type: "Experiment" | "PreData" | "PostData" | "CPA" | "Process") {
    ID.forEach((element) => {
      this.queryNeo4jService.queryOneCPA(element).then((res) => {
        this.callBacks.push(res)
      })
    })

  }
  ngOnChanges(changes: SimpleChanges) {
    if (changes['openSearch']) {
      this.callBacks = []
      this.showGraphController = []
      if (this.openSearch['selectedId'].length !== 0) {
        this.searchOne(this.openSearch['selectedId'], this.openSearch['which'])
      }
    }
  }

  getObjectKeys(obj: any): string[] {
    if (Object.keys(obj).length === 0) {
      return []
    }
    else {
      return Object.keys(obj);
    }
  }
  emm(input: string) {
    return input + '_ID'
  }

  openDialogGraph(callBack: any): void {
    let dialogRef = this.dialog.open(UnitEditDatabaseComponent, {
      width: '70%',
      height: '70%',
    })
    let instance = dialogRef.componentInstance
    instance['callBack'] = callBack
    instance['type'] = this.openSearch['which']
  }

  showGraph(cpa_id: string, sub: string) {
    if (this.showGraphController.indexOf(cpa_id + sub) === -1) {
      this.showGraphController.push(cpa_id + sub)
    }
    else {
      this.showGraphController = this.showGraphController.filter(item => item != cpa_id + sub)
    }

  }

  compressObjectValues(curveData: string): Record<string, string | Array<string>> {
    const obj: Record<string, string | Array<string>> = JSON.parse(curveData.replace(/'/g, '"'))
    let output: { [k: string]: string } = {}
    this.getObjectKeys(obj).forEach((key: string) => {
      output[key] = `${obj[key].length} items`
    })
    return output
  }
}
