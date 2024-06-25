import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitAnalyseCpaComponent } from './unit-analyse-cpa.component';

describe('UnitAnalyseCpaComponent', () => {
  let component: UnitAnalyseCpaComponent;
  let fixture: ComponentFixture<UnitAnalyseCpaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnitAnalyseCpaComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitAnalyseCpaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
