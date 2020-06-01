package main.security;

import main.security.jwt.JwtSecurityConfigurer;
import main.security.jwt.JwtTokenProvider;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.access.event.AuthenticationCredentialsNotFoundEvent;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;

@Configuration
public class SpringSecurityConfig extends WebSecurityConfigurerAdapter {

    @Autowired
    private JwtTokenProvider jwtTokenProvider;

    @Bean
    @Override
    public AuthenticationManager authenticationManagerBean() throws Exception{
        return super.authenticationManagerBean();
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.httpBasic().disable()
                .csrf().disable()
                .formLogin().disable()
                .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                .and()
                .authorizeRequests()
                .antMatchers("/libr/singin").permitAll()
                .antMatchers(HttpMethod.POST,"/libr/addJournal").hasRole("ADMIN")
                .antMatchers(HttpMethod.POST,"/libr/addBook").hasRole("ADMIN")
                .antMatchers(HttpMethod.POST,"/libr/addBookType").hasRole("ADMIN")
                .antMatchers(HttpMethod.POST,"/libr/addClient").hasRole("ADMIN")
                .antMatchers(HttpMethod.PUT,"/libr/editJournal").hasRole("ADMIN")
                .antMatchers(HttpMethod.PUT,"/libr/editBook").hasRole("ADMIN")
                .antMatchers(HttpMethod.PUT,"/libr/editBookType").hasRole("ADMIN")
                .antMatchers(HttpMethod.PUT,"/libr/editClient").hasRole("ADMIN")
                .antMatchers(HttpMethod.DELETE,"/libr/deleteJournal").hasRole("ADMIN")
                .antMatchers(HttpMethod.DELETE,"/libr/deleteBook").hasRole("ADMIN")
                .antMatchers(HttpMethod.DELETE,"/libr/deleteBookType").hasRole("ADMIN")
                .antMatchers(HttpMethod.DELETE,"/libr/deleteClient").hasRole("ADMIN")
                .antMatchers(HttpMethod.GET,"/libr/journals").permitAll()
                .antMatchers(HttpMethod.GET,"/libr/books").permitAll()
                .antMatchers(HttpMethod.GET,"/libr/bookTypes").permitAll()
                .antMatchers(HttpMethod.GET,"/libr/clients").permitAll()
                .antMatchers(HttpMethod.GET,"/libr/journal/{id}").permitAll()
                .antMatchers(HttpMethod.GET,"/libr/book/{id}").permitAll()
                .antMatchers(HttpMethod.GET,"/libr/bookType/{id}").permitAll()
                .antMatchers(HttpMethod.GET,"/libr/client/{id}").permitAll()
                .anyRequest().authenticated()
                .and()
                .apply(new JwtSecurityConfigurer(jwtTokenProvider));

    }
}
