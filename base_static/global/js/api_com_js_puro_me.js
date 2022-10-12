(async function() {
    console.clear();
    const headers = {
        authorization: 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1NTk4MTAwLCJpYXQiOjE2NjU1OTQ1MDAsImp0aSI6ImE3NjljYmEwM2EyZDRhNTRhYzVmNGQyOWY4MWM4Nzc1IiwidXNlcl9pZCI6MX0.2YtdXNn0saH2-FChyQ04gt6w89IQPFF7YesH8HBpUMo',
    };
    const config = {
        method: 'GET',
        headers: headers,
    };
    const response = await fetch(
        'http://127.0.0.1:8000/authors/api/me/',
        config
    );
    
    const json = await response.json();

    console.log('STATUS', response.status)
    console.log(json);
})();