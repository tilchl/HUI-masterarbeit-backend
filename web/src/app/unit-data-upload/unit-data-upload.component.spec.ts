import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitDataUploadComponent } from './unit-data-upload.component';

describe('UnitDataUploadComponent', () => {
  let component: UnitDataUploadComponent;
  let fixture: ComponentFixture<UnitDataUploadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnitDataUploadComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitDataUploadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
