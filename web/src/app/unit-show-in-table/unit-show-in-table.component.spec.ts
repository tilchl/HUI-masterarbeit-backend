import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitShowInTableComponent } from './unit-show-in-table.component';

describe('UnitShowInTableComponent', () => {
  let component: UnitShowInTableComponent;
  let fixture: ComponentFixture<UnitShowInTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnitShowInTableComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitShowInTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
