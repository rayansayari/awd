import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Vehicle, Reservation, Agency, Review } from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly gatewayUrl = 'http://localhost:8080/api';

  constructor(private http: HttpClient) {}

  // Vehicles
  getVehicles(): Observable<Vehicle[]> {
    return this.http.get<Vehicle[]>(`${this.gatewayUrl}/vehicles`);
  }

  getVehicleById(id: number): Observable<Vehicle> {
    return this.http.get<Vehicle>(`${this.gatewayUrl}/vehicles/${id}`);
  }

  searchVehicles(brand?: string, agencyId?: number): Observable<Vehicle[]> {
    let params = new HttpParams();
    if (brand) params = params.set('brand', brand);
    if (agencyId) params = params.set('agencyId', agencyId.toString());
    return this.http.get<Vehicle[]>(`${this.gatewayUrl}/vehicles/search`, { params });
  }

  // Reservations
  createReservation(reservation: Reservation): Observable<Reservation> {
    return this.http.post<Reservation>(`${this.gatewayUrl}/reservations`, reservation);
  }

  getUserReservations(userId: number): Observable<Reservation[]> {
    return this.http.get<Reservation[]>(`${this.gatewayUrl}/reservations/user/${userId}`);
  }

  cancelReservation(id: number): Observable<Reservation> {
    return this.http.put<Reservation>(`${this.gatewayUrl}/reservations/${id}/cancel`, {});
  }

  // Agencies
  getAgencies(): Observable<Agency[]> {
    return this.http.get<Agency[]>(`${this.gatewayUrl}/agencies`);
  }

  // Reviews
  getVehicleReviews(vehicleId: number): Observable<Review[]> {
    return this.http.get<Review[]>(`${this.gatewayUrl}/reviews/vehicle/${vehicleId}`);
  }

  createReview(review: Review): Observable<Review> {
    return this.http.post<Review>(`${this.gatewayUrl}/reviews`, review);
  }
}
