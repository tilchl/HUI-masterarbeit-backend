import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitAnalyseExpGraphComponent } from './unit-analyse-exp-graph.component';

describe('UnitAnalyseExpGraphComponent', () => {
  let component: UnitAnalyseExpGraphComponent;
  let fixture: ComponentFixture<UnitAnalyseExpGraphComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnitAnalyseExpGraphComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitAnalyseExpGraphComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
