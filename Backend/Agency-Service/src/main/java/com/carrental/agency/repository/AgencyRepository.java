package com.carrental.agency.repository;

import com.carrental.agency.domain.Agency;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface AgencyRepository extends JpaRepository<Agency, Long> {
    List<Agency> findByAddress_CityIgnoreCase(String city);
}
