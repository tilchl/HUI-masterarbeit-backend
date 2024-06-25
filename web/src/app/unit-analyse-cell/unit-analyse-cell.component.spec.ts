import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitAnalyseCellComponent } from './unit-analyse-cell.component';

describe('UnitAnalyseCellComponent', () => {
  let component: UnitAnalyseCellComponent;
  let fixture: ComponentFixture<UnitAnalyseCellComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnitAnalyseCellComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitAnalyseCellComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
