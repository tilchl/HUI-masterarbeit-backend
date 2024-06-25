import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { QueryNeo4jService } from '../app-services';
import { MatDialog } from '@angular/material/dialog';
import { UnitEditDatabaseComponent } from '../unit-edit-database/unit-edit-database.component';

@Component({
  selector: 'app-unit-analyse-process',
  templateUrl: './unit-analyse-process.component.html',
  styleUrls: ['./unit-analyse-process.component.css']
})
export class UnitAnalyseProcessComponent implements OnChanges {
  @Input() staticOrNot!: boolean
  @Input() openSearch!: { which: "Experiment" | "PreData" | "PostData" | "CPA" | "Process", selectedId: string[] }
  @Output() deleteOne: EventEmitter<string> = new EventEmitter<string>()

  callBacks: any[] = []

  topItems: string[] = [
    "Freezing_device",
    "Cooling_rate",
    "Preservation_container",
    "Storage_temperature",
    "Storage_medium",
    "Storage_duration",
    "Thawing_temperature",
    "Washing_steps",
    "Dilution_medium",
    "Dilution_factor"
  ]
  seeMore: string[] = [];
  constructor(
    private queryNeo4jService: QueryNeo4jService,
    public dialog: MatDialog,
  ) { }

  searchOne(ID: readonly string[], data_type: "Experiment" | "PreData" | "PostData" | "CPA" | "Process") {
    ID.forEach((element) => {
      this.queryNeo4jService.queryOneNode(data_type, element).then((res) => {
        this.callBacks.push(res)
      })
    })

  }
  hidden: boolean = false
  ngOnChanges(changes: SimpleChanges) {
    if (changes['openSearch']) {
      this.callBacks = []
      this.containerOffset = 0;
      this.showAnalyse = false
      this.toShow = {}
      this.isAtStart = true;
      this.hidden = false
      if (this.openSearch['selectedId'].length == 1) {
        this.isAtEnd = true;
      } else if (this.openSearch['selectedId'].length == 0) {
        this.isAtEnd = true;
      } else {
        this.isAtEnd = false;
      }

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
  delete(item: string) {
    // this.deleteOne.emit(item)
    this.hidden = true
  }

  currentIndex = 0;
  containerOffset = 0;
  cardWidth = 400;
  isAtStart = true;
  isAtEnd = true;

  slideLeft() {
    this.currentIndex = Math.max(this.currentIndex - 1, 0);
    this.containerOffset = -this.currentIndex * this.cardWidth;
    this.updateButtonStates();
  }

  slideRight() {
    this.currentIndex = Math.min(this.currentIndex + 1, this.callBacks.length - 1);
    this.containerOffset = -this.currentIndex * this.cardWidth;
    this.updateButtonStates();
  }

  updateButtonStates() {
    this.isAtStart = this.currentIndex === 0;
    this.isAtEnd = this.currentIndex === this.callBacks.length - 1;
  }

  showAnalyse: boolean = false
  toShow: any = {}

  doShow(callBack: any) {
    this.showAnalyse = true
    this.toShow = callBack
  }
  viewData() {
    this.hidden = !this.hidden
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
  seeMoreAttr() {
    this.seeMore.push('')
  }
}
