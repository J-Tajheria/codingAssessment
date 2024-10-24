import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-events-table',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div>
      <h1>HELLOOOOOO</h1>
      <table>
        <thead>
          <tr>
            <th>Event Name</th>
            <th>Status</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let event of events">
            <td>{{ event.eventsName }}</td>
            <td>{{ event.status }}</td>
            <td>{{ event.created_at }}</td>
          </tr>
        </tbody>
      </table>
    </div>  `,
  styles: ``
})
export class EventsTableComponent {
  events: any[] = [];

  constructor(private http: HttpClient){
    this.loadEvents();
  }

  loadEvents() {
    this.http.get<any[]>('http://127.0.0.1:5000/events').subscribe(events => {
      this.events = events;
    });
  }
}
