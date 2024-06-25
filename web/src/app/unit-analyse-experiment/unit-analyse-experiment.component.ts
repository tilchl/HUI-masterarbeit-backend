import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { QueryNeo4jService } from '../app-services';
import { MatDialog } from '@angular/material/dialog';
import { UnitEditDatabaseComponent } from '../unit-edit-database/unit-edit-database.component';


@Component({
  selector: 'app-unit-analyse-experiment',
  templateUrl: './unit-analyse-experiment.component.html',
  styleUrls: ['./unit-analyse-experiment.component.css']
})
export class UnitAnalyseExperimentComponent {
  @Input() staticOrNot!: boolean
  @Input() openSearch!: { which: "Experiment" | "PreData" | "PostData" | "CPA" | "Process", selectedId: string[] }
  @Output() deleteOne: EventEmitter<string> = new EventEmitter<string>()

  callBacks: any[] = []

  constructor(
    private queryNeo4jService: QueryNeo4jService,
    public dialog: MatDialog,
  ) { }

  searchOne(ID: readonly string[], data_type: "Experiment" | "PreData" | "PostData" | "CPA" | "Process") {
    ID.forEach((element) => {
      this.queryNeo4jService.queryOneExperiment(element).then((res) => {
        this.callBacks.push(res)
      })
    })

  }
  ngOnChanges(changes: SimpleChanges) {
    if (changes['openSearch']) {
      this.callBacks = []
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

  parseArray(input: any): boolean {
    try {
      if (Array.isArray(input)) {
        return true;
      }
      return false;
    } catch (error) {
      return false;
    }
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
}
