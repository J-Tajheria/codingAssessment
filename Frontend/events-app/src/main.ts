import { bootstrapApplication } from '@angular/platform-browser';
// import { appConfig } from './app/app.config';
// import { AppComponent } from './app/app.component';
import { EventsTableComponent } from './app/components/events-table.component'
import { provideHttpClient } from '@angular/common/http';

bootstrapApplication(EventsTableComponent, {
  providers: [provideHttpClient()]
}).catch((err) => console.error(err));
