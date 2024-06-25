import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeiteAboutThisComponent } from './seite-about-this.component';

describe('SeiteAboutThisComponent', () => {
  let component: SeiteAboutThisComponent;
  let fixture: ComponentFixture<SeiteAboutThisComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SeiteAboutThisComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SeiteAboutThisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
