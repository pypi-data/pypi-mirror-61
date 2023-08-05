#!/usr/bin/env python
# -*- coding: utf-8 -*-
# description: 一个守护进程的简单包装类, 具备常用的start|stop|restart|status功能, 使用方便
#             需要改造为守护进程的程序只需要重写基类的run函数就可以了
# date: 2015-10-29
# usage: 启动: python daemon_class.py start
#       关闭: python daemon_class.py stop
#       状态: python daemon_class.py status
#       重启: python daemon_class.py restart
#       查看: ps -axj | grep daemon_class

import atexit, os, sys, time, signal
from .command import execute
from .CommonLogger import debug, info, warn, error


class CDaemon:
    '''
    a generic daemon class.
    usage: subclass the CDaemon class and override the run() method
    stderr  表示错误日志文件绝对路径, 收集启动过程中的错误日志
    verbose 表示将启动运行过程中的异常错误信息打印到终端,便于调试,建议非调试模式下关闭, 默认为1, 表示开启
    save_path 表示守护进程pid文件的绝对路径
    '''

    def __init__(self, save_path, stdin=os.devnull, stdout=sys.stdout, stderr=sys.stderr, home_dir='/sf/log',
                 umask=0x12,
                 verbose=0):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = save_path  # pid文件绝对路径
        self.home_dir = home_dir
        self.verbose = verbose  # 调试开关
        self.umask = umask
        self.daemon_alive = True

    def daemonize(self):
        debug("start daemonize")
        try:
            pid = os.fork()
            if pid > 0:
                return False
        except OSError as e:
            sys.stderr.write('fork #1 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)

        debug("fork1 finish,goto fork2")
        os.chdir(self.home_dir)
        os.setsid()
        os.umask(self.umask)

        # try:
        #     pid = os.fork()
        #     if pid > 0:
        #         return False
        # except OSError, e:
        #     sys.stderr.write('fork #2 failed: %d (%s)\n' % (e.errno, e.strerror))
        #     sys.exit(1)

        debug("fork2 finish")
        sys.stdout.flush()
        sys.stderr.flush()

        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        if self.stderr:
            se = open(self.stderr, 'a+', 0)
        else:
            se = so

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        def sig_handler(signum, frame):
            self.daemon_alive = False
            exit(0)

        signal.signal(signal.SIGTERM, sig_handler)
        signal.signal(signal.SIGINT, sig_handler)

        debug("daemon process started")

        atexit.register(self.del_pid)
        pid = str(os.getpid())
        open(self.pidfile, 'w+').write('%s\n' % pid)
        return True

    def get_pid(self):
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        except SystemExit:
            pid = None
        return pid

    def del_pid(self):
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)

    def start(self, *args, **kwargs):
        # if self.verbose >= 1:
        #     print 'ready to starting ......'
        # check for a pid file to see if the daemon already runs
        pid = self.get_pid()
        if pid:
            msg = 'pid file %s already exists, is it already running?\n'
            sys.stderr.write(msg % self.pidfile)
            sys.exit(1)
        # start the daemon
        if self.daemonize():
            self.run(*args, **kwargs)

    def stop(self):
        debug('stopping ...')
        pid = self.get_pid()
        if not pid:
            msg = 'pid file [%s] does not exist. Not running?\n' % self.pidfile
            sys.stderr.write(msg)
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)
            return
        # try to kill the daemon process
        try:
            i = 0
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
                i = i + 1
                if i % 10 == 0:
                    os.kill(pid, signal.SIGHUP)
        except OSError as err:
            err = str(err)
            if err.find('No such process') > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                error("get err", err)
                sys.exit(1)
            debug("finish stop")

    def restart(self, *args, **kwargs):
        self.stop()
        self.start(*args, **kwargs)

    def is_running(self):
        pid = self.get_pid()
        # print(pid)
        return pid and os.path.exists('/proc/%d' % pid)

    def run(self, *args, **kwargs):
        'NOTE: override the method in subclass'
        print('base class run()')


class ClientDaemon(CDaemon):
    def __init__(self, name, save_path, stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, home_dir='.',
                 umask=0x12,
                 verbose=1):
        CDaemon.__init__(self, save_path, stdin, stdout, stderr, home_dir, umask, verbose)
        self.name = name  # 派生守护进程类的名称

    def run(self, output_fn, **kwargs):
        fd = open(output_fn, 'w')
        while True:
            line = time.ctime() + '\n'
            fd.write(line)
            fd.flush()
            time.sleep(1)
        fd.close()

    @classmethod
    def daemon_run(cls, name, method, *args, **kwargs):
        class tmp_daemon(cls):
            def run(self):
                return method(*args, **kwargs)

        ins = tmp_daemon(name, '/tmp/vst_daemon_run_{name}.pid'.format(name=name))
        ins.start()

    @classmethod
    def daemon_stop(cls, name):
        if os.path.exists('/tmp/vst_daemon_run_{name}.pid'.format(name=name)):
            execute('kill `cat /tmp/vst_daemon_run_{name}.pid`'.format(name=name))
            execute('rm -f /tmp/vst_daemon_run_{name}.pid'.format(name=name))


if __name__ == '__main__':
    help_msg = 'Usage: python %s <start|stop|restart|status>' % sys.argv[0]
    if len(sys.argv) != 2:
        print(help_msg)
        sys.exit(1)
    p_name = 'clientd'  # 守护进程名称
    pid_fn = '/tmp/daemon_class.pid'  # 守护进程pid文件的绝对路径
    log_fn = '/tmp/daemon_class.log'  # 守护进程日志文件的绝对路径
    err_fn = '/tmp/daemon_class.err.log'  # 守护进程启动过程中的错误日志,内部出错能从这里看到
    cD = ClientDaemon(p_name, pid_fn, stderr=err_fn, verbose=1)

    if sys.argv[1] == 'start':
        cD.start(log_fn)
    elif sys.argv[1] == 'stop':
        cD.stop()
    elif sys.argv[1] == 'restart':
        cD.restart(log_fn)
    elif sys.argv[1] == 'status':
        alive = cD.is_running()
        if alive:
            print('process [%s] is running ......' % cD.get_pid())
        else:
            print('daemon process [%s] stopped' % cD.name)
    else:
        print('invalid argument!')
        print(help_msg)
