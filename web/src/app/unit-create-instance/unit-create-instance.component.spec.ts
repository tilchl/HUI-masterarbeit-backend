import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitCreateInstanceComponent } from './unit-create-instance.component';

describe('UnitCreateInstanceComponent', () => {
  let component: UnitCreateInstanceComponent;
  let fixture: ComponentFixture<UnitCreateInstanceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnitCreateInstanceComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitCreateInstanceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
