package com.footballst.footballst.api.event;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;


public interface EventRepository extends JpaRepository<Event, Long> {
    List<Event> findByMatchId(Long matchId);


}
