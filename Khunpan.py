__author__ = 'Rudolf Hart'

from Tkinter import *
import Tk
import Board
import Piece
import Game
import Tk.TargetBoard
import Tk.PlayBoard

class Khunpan:
    def __init__(self):
        self.title = "Khun Pan";
        self.add_menu()
        self.add_toolbar()
        self.init_config()
        self.game_new();

    def init_config(self):
        self.config = { zoom : 20 }

    def get_config(self,key):
        return self.config[key]
}

#  menu definition
sub add_menu {
    my ($self) = @_;
    my $menubar_items = [
        [   cascade    => '~Game',
            -tearoff   => 0,
            -menuitems => [
                [ command => '~Default',  -command => [ \&game_new,  $self ] ],
#                [ command => '~Load', -command => [ \&game_load, $self ] ],
#                [ command => '~Save', -command => [ \&game_save, $self ] ],
                q{-},
                [ command => '~Reset', -command => [ \&game_reset, $self ] ],
                q{-},
                [ command => '~Quit', -command => [ \&game_quit, $self ] ],
            ],

        ],
        [   cascade    => '~Replay',
            -tearoff   => 0,
            -menuitems => [
                [ command => '~Play',, -command => [ \&replay_play, $self ] ],
                q{-},
                [ command => '~Load', -command => [ \&replay_load, $self ] ],
                [ command => '~Save', -command => [ \&replay_save, $self ] ],

            ],
        ],
        [   cascade    => '~Help',
            -tearoff   => 0,
            -menuitems => [
                [   command => '~Quick',
                    -command => [ \&help_quick, $self ]
                ],
                [   command => '~Contents',
                    -command => [ \&help_contents, $self ]
                ],
                q{-},
                [ command => '~About', -command => [ \&help_about, $self ] ],
            ],
        ],
    ];

    my $menubar = $self->Menu( -menuitems => $menubar_items );
    $self->configure( -menu => $menubar );
    return;
}


sub add_toolbar {
  my ($self) = @_;
  my $game;

  my $gamedir = dirname($PROGRAM_NAME).'/games';
  $self->{toolbar} = $self->Frame();
  $self->{toolbar}->Optionmenu(
                               -options => [ _game_list() ],
                               -variable => \$game,
                              )->pack(-side=>'left');
  $self->{toolbar}->Button(
                           -text=>'Load Game',
                           -command=> sub {
                             $self->Khunpan::game_load($game);
                           },
                          )->pack(-side=>'left');
  $self->{toolbar}->pack(-side => 'top', -fill => 'x');
  return;
}

sub init_boards {
    my ($self) = @_;

	if ($self->{boards}){
        $self->{boards}->destroy();
	}
    $self->{boards} = $self->Frame()->pack(-side=>'bottom',-fill=>'both');
    my $board  = $self->{game}->get_board();
    my $target = $self->{game}->get_target();

    $self->{tkboard} = $self->{boards}->PlayBoard(
        -board => $board,
        -game  => $self->{game},
        -zoom  => $self->get_config('zoom')
    )->pack( -side => 'left' );
    $self->{boards}->Label(
        -text       => '  =>  ',
        -background => 'white'
    )->pack( -side => 'left', -fill => 'y' );
    $self->{boards}->TargetBoard(
        -board => $target,
        -game  => $self->{game},
        -zoom  => $self->get_config('zoom')
    )->pack( -side => 'left' );
    return;
}

### Callbacks ###

## Game ##

sub game_new {
    my ($self) = @_;
    $self->{game} = Game->new();
    $self->{game}->load();
    $self->init_boards();
    $self->configure(-title=>$self->{title}.': default');
    return;
}

sub game_load {
    my ($self,$game) = @_;
    my $filename;
    if($game) {
      $filename = dirname($PROGRAM_NAME)."/games/$game.game";
    }
    else {
      $filename = $self->getOpenFile(
        -initialdir => dirname($PROGRAM_NAME).'/games',
        -defaultextension => '.game',
        -filetypes        => [
            [ Games            => [ '.game', ] ],
            [ 'User Games' => '_user.game' ],
        ],
        -initialfile => '00-ling.game',
       );

      if (not $filename ) { return; }
      $game = basename $filename,'.game';
    }

    $self->{game} = Game->new($filename);
    $self->{game}->load();
    $self->init_boards();
    $self->configure(-title=>$self->{title}.": $game");
    return;
}

sub game_save {
    my ($self) = @_;
    my $filename = $self->getSaveFile(
        -initialdir => dirname($PROGRAM_NAME).'/games',
        -defaultextension => '_user.game',
        -filetypes        => [ [ Games => [ '.game' ] ],
                               [ 'User Games' => '_user.game' ] ],
    );
    if (not $filename ) { return; }
    $filename = $filename;
    $self->{game}->save($filename);
    return;
}

sub game_reset {
    my ($self) = @_;
    $self->{game}->load();
    $self->init_boards();
    $self->{game}->clear_history();
    return;
}

sub game_quit {
    my ($self) = @_;
    exit 0;
}

## Replay ##

sub replay_play {
    my ($self) = @_;

    Readonly my $REPLAY_STEP_TIME => 100;

    $self->{game}->load();
    $self->init_boards();
    $self->{game}->rewind();

    $self->after( $REPLAY_STEP_TIME,
        [ \&Tk::PlayBoard::replay_move, $self->{tkboard}, $self->{game} ] );
    return;
}

sub replay_load {
    my ($self) = @_;
    my $filename = $self->getOpenFile(
        -initialdir => dirname($PROGRAM_NAME).'/histories',
        -defaultextension => '.sol',
        -filetypes        => [ [ 'Solutions' => [ '.sol' ] ],
                               [ 'Game History' => [ '.hist' ] ],
                             ],
    );
    if (not $filename ) { return; }
    if ( $self->{game}->load_history($filename) != 0 ) {
        $self->messageBox(
            -type    => 'OK',
            -icon    => 'error',
            -message => 'History requires game '
                . basename $filename
                . ".\n\n"
                . '                  NOT LOADED!'
        );
    }
    return;
}

sub replay_save {
    my ($self) = @_;
    my $filename = $self->getSaveFile(
        -initialdir => dirname($PROGRAM_NAME).'/histories',
        -defaultextension => '.hist',
        -filetypes        => [ [ 'Solutions' => [ '.sol' ] ],
                               [ 'Game History' => [ '.hist' ] ] ]
    );
    if (not $filename ) { return; }
    $filename = $filename;
    $self->{game}->save_history($filename);
    return;
}

## Help ##

sub help_quick {
    my ($self) = @_;
    my $help = <<'_ABOUT_';

  Move the red piece (Khun Pan) into the position indicated at the right.
  To move a piece click on it near the free area.

  You will get a message about success if you move all the pieces to the
  position indicated on the right.

_ABOUT_
    $self->messageBox( -type => 'OK', -icon => 'info', -message => $help );
    return;
}

sub help_contents {
    my ($self) = @_;
    use App::PodPreview qw(podpreview);
    podpreview($PROGRAM_NAME);
    return;
}

sub help_about {
    my ($self) = @_;
    my $about = <<"_ABOUT_";
                Khun Pan V$REL_VERSION
           Copyright 2004 Rudolf Hart

   If you have problems and understand German
  you might have a look at http://www.khunpan.de/

_ABOUT_
    $self->messageBox( -type => 'OK', -icon => 'info', -message => $about );
    return;
}
sub _game_list {
    my $gamedir = dirname($PROGRAM_NAME).'/games';
    opendir(my $dir,$gamedir) || die "Reading game directory $gamedir failed\n";
    my @games = sort readdir $dir;
    @games = grep { not m{\A\.}xms } @games;
    for my $ind ( 0 .. @games - 1 ) {
    	$games[$ind]=~s{.game\z}{}xms;
	}
    return @games;
}

