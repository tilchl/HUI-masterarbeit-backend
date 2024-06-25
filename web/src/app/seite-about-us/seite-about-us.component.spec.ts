import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeiteAboutUsComponent } from './seite-about-us.component';

describe('SeiteAboutUsComponent', () => {
  let component: SeiteAboutUsComponent;
  let fixture: ComponentFixture<SeiteAboutUsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SeiteAboutUsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SeiteAboutUsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
