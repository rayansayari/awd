package com.carrental.agency.dto;

import lombok.*;

@Getter @Setter @NoArgsConstructor @AllArgsConstructor @Builder
public class AgencyDTO {
    private Long id;
    private String name;
    private String code;
    private String email;
    private String phone;
    private String city;
    private String street;
    private String zipCode;
    private String openingHours;
    private Boolean active;
}
