package com.carrental.agency.service.impl;

import com.carrental.agency.domain.Address;
import com.carrental.agency.domain.Agency;
import com.carrental.agency.dto.AgencyDTO;
import com.carrental.agency.repository.AgencyRepository;
import com.carrental.agency.service.AgencyService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class AgencyServiceImpl implements AgencyService {
    private final AgencyRepository agencyRepository;

    @Override
    public List<AgencyDTO> getAllAgencies() {
        return agencyRepository.findAll().stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    @Override
    public AgencyDTO getAgencyById(Long id) {
        Agency a = agencyRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Agence introuvable: " + id));
        return mapToDTO(a);
    }

    @Override
    public List<AgencyDTO> getAgenciesByCity(String city) {
        return agencyRepository.findByAddress_CityIgnoreCase(city).stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    @Override
    public AgencyDTO createAgency(AgencyDTO dto) {
        Address addr = Address.builder()
                .street(dto.getStreet())
                .city(dto.getCity())
                .zipCode(dto.getZipCode())
                .build();
        Agency a = Agency.builder()
                .name(dto.getName())
                .code(dto.getCode())
                .email(dto.getEmail())
                .phone(dto.getPhone())
                .openingHours(dto.getOpeningHours())
                .address(addr)
                .build();
        return mapToDTO(agencyRepository.save(a));
    }

    @Override
    public AgencyDTO updateAgency(Long id, AgencyDTO dto) {
        Agency a = agencyRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Agence introuvable: " + id));
        a.setName(dto.getName());
        a.setEmail(dto.getEmail());
        a.setPhone(dto.getPhone());
        return mapToDTO(agencyRepository.save(a));
    }

    @Override
    public void deleteAgency(Long id) {
        agencyRepository.deleteById(id);
    }

    private AgencyDTO mapToDTO(Agency a) {
        return AgencyDTO.builder()
                .id(a.getId())
                .name(a.getName())
                .code(a.getCode())
                .email(a.getEmail())
                .phone(a.getPhone())
                .city(a.getAddress() != null ? a.getAddress().getCity() : null)
                .street(a.getAddress() != null ? a.getAddress().getStreet() : null)
                .zipCode(a.getAddress() != null ? a.getAddress().getZipCode() : null)
                .openingHours(a.getOpeningHours())
                .active(a.getActive())
                .build();
    }
}
