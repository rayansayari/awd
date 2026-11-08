export interface User {
  id: number;
  username: string;
  email: string;
  firstName?: string;
  lastName?: string;
  phoneNumber?: string;
  driverLicenseNumber?: string;
  roles: string[];
}

export interface Vehicle {
  id: number;
  brand: string;
  model: string;
  year: number;
  licensePlate: string;
  pricePerDay: number;
  color?: string;
  seatingCapacity?: number;
  transmission?: string;
  fuelType?: string;
  status: 'AVAILABLE' | 'RENTED' | 'MAINTENANCE' | 'OUT_OF_SERVICE';
  agencyId: number;
  imageUrl?: string;
}

export interface Reservation {
  id?: number;
  reservationNumber?: string;
  userId: number;
  vehicleId: number;
  pickupAgencyId?: number;
  returnAgencyId?: number;
  startDate: string;
  endDate: string;
  totalDays?: number;
  dailyRate?: number;
  totalPrice?: number;
  status?: 'PENDING' | 'CONFIRMED' | 'ACTIVE' | 'COMPLETED' | 'CANCELLED';
}

export interface Payment {
  id?: number;
  transactionId?: string;
  reservationId: number;
  userId: number;
  amount: number;
  paymentMethod: 'CREDIT_CARD' | 'PAYPAL' | 'CASH_ON_PICKUP';
  status: 'PENDING' | 'PAID' | 'FAILED' | 'REFUNDED';
  invoiceNumber?: string;
}

export interface Agency {
  id: number;
  name: string;
  code: string;
  email?: string;
  phone?: string;
  city: string;
  street: string;
  openingHours?: string;
  active: boolean;
}

export interface Review {
  id?: string;
  userId: number;
  targetType: 'VEHICLE' | 'AGENCY';
  targetId: number;
  rating: number;
  comment: string;
  createdAt?: string;
}
