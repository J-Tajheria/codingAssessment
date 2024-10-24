import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-events-table',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="container">
      <h1 class="events-header">Console Management System</h1>
      <h2 class="events-header"> Add a new item to the system </h2>
      <div>
        <input [(ngModel)]="newEventName" placeholder="Event Name "/>
        <input [(ngModel)]="newEventStatus" placeholder="Event Status "/>
        <button (click)="addEvent()"> Add </button>
      </div>
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
            <td>
              <img src="trash-2.svg" alt="Trashbin" (click)="deleteEvent(event.id)"/>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  `,
  styleUrl: './events-table.components.css'
})
export class EventsTableComponent {
  events: any[] = [];
  newEventName: string = '';
  newEventStatus: string = '';

  constructor(private http: HttpClient){
    this.loadEvents();
  }

  loadEvents() {
    this.http.get<any[]>('http://127.0.0.1:5000/events').subscribe(events => {
      this.events = events;
    });
  }

  addEvent() {
    const newEvent = {
      eventsName: this.newEventName,
      status: this.newEventStatus,
      created_at: new Date().toISOString().slice(0, 19).replace('T', ' ')
    };

    this.http.post('http://127.0.0.1:5000/events', newEvent).subscribe(response => {
      console.log(response);
      this.loadEvents(); 
      this.newEventName = ''; 
      this.newEventStatus = '';

    });
  }

  deleteEvent(id: number) {
    this.http.delete(`http://127.0.0.1:5000/events/${id}`).subscribe(() => {
      this.loadEvents();
    });
  }
}
