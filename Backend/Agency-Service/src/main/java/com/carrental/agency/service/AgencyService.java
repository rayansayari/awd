package com.carrental.agency.service;

import com.carrental.agency.dto.AgencyDTO;
import java.util.List;

public interface AgencyService {
    List<AgencyDTO> getAllAgencies();
    AgencyDTO getAgencyById(Long id);
    List<AgencyDTO> getAgenciesByCity(String city);
    AgencyDTO createAgency(AgencyDTO dto);
    AgencyDTO updateAgency(Long id, AgencyDTO dto);
    void deleteAgency(Long id);
}
