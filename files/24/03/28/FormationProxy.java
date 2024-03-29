package com.example.msscolarite.entities;

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import org.springframework.cloud.loadbalancer.annotation.LoadBalancerClient;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "ms-formation")
@LoadBalancerClient(name="ms-formation")
public interface FormationProxy {

    @GetMapping("formations/{id}")
   @CircuitBreaker(name="fall", fallbackMethod = "fallbackFormation" )
    public Formation getF(@PathVariable("id") Long id);
    default Formation fallbackFormation( @PathVariable("id") Long idf,
                                         Throwable throwable){

        if(idf.equals(1L))
            return new Formation(1L,"web1") ;
        else if(idf.equals(2L))
            return new Formation(2L,"intergiciel") ;
        return new Formation(3L,"nodejs") ;
    }
}
