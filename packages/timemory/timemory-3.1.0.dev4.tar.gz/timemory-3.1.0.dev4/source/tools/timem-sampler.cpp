// MIT License
//
// Copyright (c) 2020, The Regents of the University of California,
// through Lawrence Berkeley National Laboratory (subject to receipt of any
// required approvals from the U.S. Dept. of Energy).  All rights reserved.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#define TIMEM_BUNDLER                                                                    \
    tim::auto_tuple<real_clock, system_clock, user_clock, cpu_clock, cpu_util, peak_rss, \
                    page_rss, user_mode_time, kernel_mode_time, virtual_memory,          \
                    read_bytes, written_bytes>

#include "timem.hpp"

//--------------------------------------------------------------------------------------//

static double      sample_rate   = 5.0 * tim::units::sec;
static double      sample_delay  = 1.0 * tim::units::sec;
static int64_t     total_samples = 0;
static std::string prefix        = "";
static wall_clock  interval      = {};

//--------------------------------------------------------------------------------------//

inline std::string
compose_prefix()
{
    std::stringstream ss;
    ss << command().c_str() << "@" << std::setprecision(3) << interval.get() << "sec";
    return ss.str();
}

//--------------------------------------------------------------------------------------//

inline void
sampler(int signum)
{
    if(signum == TIMEM_SIGNAL)
    {
        if(get_measure())
        {
            interval.stop();
            get_measure()->stop();

            if((debug() && verbose() > 1) || (verbose() > 2))
                std::cerr << "[SAMPLE][" << getpid() << "]> " << *get_measure()
                          << std::endl;
            else if(debug())
                fprintf(stderr, "[%i]> sampling...\n", getpid());

            // delete get_measure();
        }

        // get_measure() = new comp_tuple_t(compose_prefix());
        get_measure()->rekey(compose_prefix());
        get_measure()->start();
        interval.start();
    }
    else
    {
        perror("timem sampler caught signal that was not TIMEM_SIGNAL...");
        signal(signum, SIG_DFL);
        raise(signum);
    }
}

//--------------------------------------------------------------------------------------//

inline void
sampler(int signum, siginfo_t*, void*)
{
    if(signum == TIMEM_SIGNAL)
    {
        if(get_measure())
        {
            interval.stop();
            get_measure()->stop();

            if((debug() && verbose() > 1) || (verbose() > 2))
                std::cerr << "[SAMPLE][" << getpid() << "]> " << *get_measure()
                          << std::endl;
            else if(debug())
                fprintf(stderr, "[%i]> sampling...\n", getpid());

            // delete get_measure();
        }

        // get_measure() = new comp_tuple_t(compose_prefix());
        get_measure()->rekey(compose_prefix());
        get_measure()->start();
        interval.start();
    }
    else
    {
        perror("timem sampler caught signal that was not TIMEM_SIGNAL...");
        signal(signum, SIG_DFL);
        raise(signum);
    }
}

//--------------------------------------------------------------------------------------//

void
parent_process(pid_t pid, int status)
{
    int ret = diagnose_status(status);

    if((debug() && verbose() > 1) || verbose() > 2)
        std::cerr << "[AFTER STOP][" << pid << "]> " << *get_measure() << std::endl;

    delete get_measure();
    tim::timemory_finalize();

    exit(ret);
}

//--------------------------------------------------------------------------------------//

declare_attribute(noreturn) void child_process(int argc, char** argv)
{
    if(argc < 2)
        exit(0);

    // the argv list first argument should point to filename associated
    // with file being executed the array pointer must be terminated by
    // NULL pointer

    std::stringstream shell_cmd;
    char**            argv_list = (char**) malloc(sizeof(char**) * (argc));
    for(int i = 0; i < argc; i++)
    {
        argv_list[i] = strdup(argv[i]);
        shell_cmd << argv[i] << " ";
    }
    argv_list[argc - 1] = nullptr;

    // launches the command with the shell, this is the default because it enables aliases
    auto launch_using_shell = [&]() {
        int         ret             = -1;
        int         argc_shell      = 5;
        char**      argv_shell_list = new char*[argc];
        std::string _shell          = tim::get_env<std::string>("SHELL", getusershell());

        if(debug() || verbose() > 0)
            fprintf(stderr, "using shell: %s\n", _shell.c_str());

        argv_shell_list[argc_shell - 1] = nullptr;
        if(_shell.length() > 0)
        {
            if(debug())
                PRINT_HERE("%s", "");

            std::string _interactive = "-i";
            std::string _command     = "-c";
            argv_shell_list[0]       = strdup(_shell.c_str());
            argv_shell_list[1]       = strdup(_interactive.c_str());
            argv_shell_list[2]       = strdup(_command.c_str());
            argv_shell_list[3]       = strdup(shell_cmd.str().c_str());
            argv_shell_list[4]       = nullptr;

            if(debug())
                PRINT_HERE("%s", "");

            explain(0, argv_shell_list[0], argv_shell_list);
            ret = execvp(argv_shell_list[0], argv_shell_list);
            // ret = execv(argv_shell_list[0], argv_shell_list);
            explain(ret, argv_shell_list[0], argv_shell_list);

            if(ret != 0)
            {
                PRINT_HERE("return code: %i", ret);
                explain(ret, argv_shell_list[0], argv_shell_list);
                ret = execv(argv_shell_list[0], argv_shell_list);
            }

            if(ret != 0)
            {
                PRINT_HERE("return code: %i", ret);
                explain(ret, argv_shell_list[0], argv_shell_list);
                ret = execve(argv_shell_list[0], argv_shell_list, environ);
            }

            if(debug())
                PRINT_HERE("return code: %i", ret);
        }
        else
        {
            fprintf(stderr, "getusershell failed!\n");
        }

        if(debug())
            PRINT_HERE("%s", "");

        return ret;
    };

    // this will launch the process and inherit the environment but aliases will not
    // be available
    auto launch_without_shell = [&]() {
        int ret = execvp(argv_list[0], argv_list);
        // explain error if enabled
        explain(ret, argv_list[0], argv_list);
        return ret;
    };

    // default return code
    int ret = -1;

    // determine if the shell should be tested first
    bool try_shell = use_shell();

    if(try_shell)
    {
        // launch the command with shell. If that fails, launch without shell
        ret = launch_using_shell();
        if(ret < 0)
        {
            if(debug())
                puts("Error launching with shell! Trying without shell...");
            ret = launch_without_shell();
        }
    }
    else
    {
        // launch the command without shell. If that fails, launch with shell
        ret = launch_without_shell();
        if(ret < 0)
        {
            if(debug())
                puts("Error launching without shell! Trying with shell...");
            ret = launch_using_shell();
        }
    }

    explain(ret, argv_list[0], argv_list);

    exit(ret);
}

//--------------------------------------------------------------------------------------//

int
main(int argc, char** argv)
{
    master_pid() = getpid();

    // set some defaults
    tim::settings::banner()      = false;
    tim::settings::file_output() = true;
    tim::settings::json_output() = true;
    tim::settings::cout_output() = true;
    tim::settings::scientific()  = false;
    tim::settings::width()       = 12;
    tim::settings::precision()   = 6;

    // parse for settings configurations
    if(argc > 1)
        tim::timemory_init(argc, argv);

    // override a some settings
    tim::settings::suppress_parsing() = true;
    tim::settings::auto_output()      = true;

    tim::enable_signal_detection();

    tim::manager::get_storage<comp_tuple_t>::initialize();
    tim::manager::instance()->set_write_metadata(-1);

    auto usage = [](int errcode) {
        std::stringstream ss;
        ss << std::setw(20) << std::left << "-h/--help" << std::setw(40) << std::right
           << ":  this message\n";
        ss << std::setw(20) << std::left << "-j/--json" << std::setw(40) << std::right
           << ":  explicit JSON output\n";
        ss << std::setw(20) << std::left << "-t/--text" << std::setw(40) << std::right
           << ":  text output\n";
        ss << std::setw(20) << std::left << "-s/--stdout" << std::setw(40) << std::right
           << ":  stdout output\n";
        ss << std::setw(20) << std::left << "-r/--rate N" << std::setw(40) << std::right
           << ":  rate (in seconds) to sample\n";
        ss << std::setw(20) << std::left << "-d/--delay N" << std::setw(40) << std::right
           << ":  delay (in seconds) before sampling\n";
        ss << std::setw(20) << std::left << "-m/--max-samples N" << std::setw(40)
           << std::right << ":  maximum number of samples\n";
        ss << std::setw(20) << std::left << "-f/--folder FOLDER" << std::setw(40)
           << std::right << ":  folder name for output\n";
        std::cout << "timem-sampler <ARGS> <EXECUTABLE>\n" << ss.str();
        exit(errcode);
    };

    auto setup_explicit = []() {
        static bool once = false;
        if(!once)
        {
            tim::settings::json_output() = false;
            tim::settings::cout_output() = false;
            tim::settings::text_output() = false;
            once                         = true;
        }
    };

    int offset = 1;
    if(argc > 1)
    {
        for(int i = 1; i < argc; ++i)
        {
            std::string arg = argv[i];
            // finished processing options
            if(arg[0] != '-')
                break;

            auto args = tim::delimit(arg, "=");

            if(args.size() == 1)
            {
                if(arg == "-h" || arg == "--help")
                {
                    usage(EXIT_SUCCESS);
                }
                else if(arg == "-j" || arg == "--json")
                {
                    setup_explicit();
                    tim::settings::json_output() = true;
                    continue;
                }
                else if(arg == "-t" || arg == "--text")
                {
                    setup_explicit();
                    tim::settings::text_output() = true;
                    continue;
                }
                else if(arg == "-s" || arg == "--stdout")
                {
                    setup_explicit();
                    tim::settings::cout_output() = true;
                    continue;
                }
            }

            if(args.size() == 1 && i + 1 >= argc)
            {
                usage(EXIT_FAILURE);
            }
            else if(args.size() == 1)
            {
                args.push_back(argv[++i]);
                offset += 2;
            }
            else
            {
                offset += 1;
            }

            if(arg == "-r" || arg == "--rate")
            {
                sample_rate = tim::from_string<double>(args.back());
            }
            else if(arg == "-f" || arg == "--folder")
            {
                tim::settings::output_path() = args.back();
                if(!tim::settings::json_output() && !tim::settings::file_output())
                {
                    tim::settings::json_output() = true;
                    tim::settings::file_output() = true;
                }
            }
            else if(arg == "-d" || arg == "--delay")
            {
                sample_delay = tim::from_string<double>(args.back());
            }
            else if(arg == "-m" || arg == "--max-samples")
            {
                tim::settings::output_path() = args.back();
                total_samples                = tim::from_string<int64_t>(args.back());
            }
            else
            {
                usage(EXIT_FAILURE);
            }
        }

        command() = std::string(const_cast<const char*>(argv[offset]));
    }
    else
    {
        exit(EXIT_SUCCESS);
    }

    pid_t pid = fork();

    if(pid != 0)
    {
        tim::get_rusage_type() = RUSAGE_CHILDREN;
        worker_pid()           = pid;
        tim::get_rusage_pid()  = pid;
    }

    int    _argc = argc - offset;
    char** _argv = argv + offset;

    if(pid != 0 && debug())
    {
        for(int i = 0; i < _argc; ++i)
            printf("argv[%i] = %s\n", i, _argv[i]);
    }

    if(pid == -1)  // pid == -1 means error occured
    {
        puts("failure forking, error occured!");
        exit(EXIT_FAILURE);
    }
    else if(pid == 0)  // pid == 0 means child process created
    {
        child_process(_argc, _argv);
    }
    else  // means parent process
    {
        // struct sigaction& sa = timem_signal_action();
        struct sigaction timem_sa;
        struct sigaction orig_sa;

        // Install timer_handler as the signal handler for TIMEM_SIGNAL.

        memset(&timem_sa, 0, sizeof(timem_sa));
        // sigfillset(&timem_sa.sa_mask);
        // sigdelset(&timem_sa.sa_mask, TIMEM_SIGNAL);

        timem_sa.sa_handler   = &sampler;
        timem_sa.sa_sigaction = &sampler;
        timem_sa.sa_flags     = SA_RESTART | SA_SIGINFO;

        sigaction(TIMEM_SIGNAL, &timem_sa, &orig_sa);

        // itimerval& _timer = timem_itimer();
        struct itimerval _timer;

        double fdelay = sample_delay;
        double ffreq  = sample_rate;

        int delay_sec  = (fdelay * 1.0e6) / 1000000.;
        int delay_usec = int(fdelay * 1.0e6) % 1000000;

        int freq_sec  = (ffreq * 1.0e6) / 1000000.;
        int freq_usec = int(ffreq * 1.0e6) % 1000000;

        if(debug() || verbose() > 0)
        {
            fprintf(stderr, "timem sampler delay     : %i sec + %i usec\n", delay_sec,
                    delay_usec);
            fprintf(stderr, "timem sampler frequency : %i sec + %i usec\n", freq_sec,
                    freq_usec);
        }

        // Configure the timer to expire after designated delay...
        _timer.it_value.tv_sec  = delay_sec;
        _timer.it_value.tv_usec = delay_usec;

        // ... and every designated interval after that
        _timer.it_interval.tv_sec  = freq_sec;
        _timer.it_interval.tv_usec = freq_usec;

        get_measure() = new comp_tuple_t(compose_prefix());
        interval.start();

        // start the interval timer
        int itimer_stat = setitimer(TIMEM_ITIMER, &_timer, nullptr);

        if(debug())
            fprintf(stderr, "Sample configuration return value: %i\n", itimer_stat);

        // pause until first interrupt delivered
        if(fdelay > 0.0)
            pause();

        // loop while the errno is not EINTR (interrupt) and status designates
        // it was stopped because of TIMEM_SIGNAL
        int status = 0;
        int errval = 0;
        do
        {
            status = 0;
            errval = waitpid_eintr(status);
        } while(errval == EINTR && diagnose_status(status, debug()) == TIMEM_SIGNAL);

        if((debug() && verbose() > 1) || verbose() > 2)
            std::cerr << "[BEFORE STOP][" << pid << "]> " << *get_measure() << std::endl;

        signal(TIMEM_SIGNAL, SIG_IGN);
        interval.stop();
        get_measure()->stop();

        parent_process(pid, status);
    }
}

//--------------------------------------------------------------------------------------//
