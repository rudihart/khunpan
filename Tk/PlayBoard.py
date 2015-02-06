__author__ = 'Rudolf Hart'

import Tk.Board


class PlayBoard(Tk.Board):
    VERSION = '1.0.0'
    SIZE_FACTOR = 5
    OFFSET = 0.1
    REPLAY_TIME_STEP = 1000

sub scale_board {
    my ($self) = @_;
    my $zoom = $SIZE_FACTOR * $self->cget('-zoom');
    $self->scale( 'board', 0, 0, $zoom, $zoom );
    return;
}

sub scale_piece {
    my ( $self, $piece ) = @_;

    my $zoom = $self->cget('-zoom');
    $self->scale( $piece->{name}, 0, 0, $zoom, $zoom );
    return;
}

sub add_sensors {
    my ( $self, $piece ) = @_;
    my ( $sx,   $sy )    = $piece->get_size();
    my ( $xpos, $ypos )  = $piece->get_position();
    my $piececolor = '#cb8';
    my $zoom       = $self->cget('-zoom');

    my $idn = $self->createRectangle(
        $xpos * $SIZE_FACTOR + 1,
        $ypos * $SIZE_FACTOR + $OFFSET,
        ( $xpos + $sx ) * $SIZE_FACTOR - 1,
        $ypos * $SIZE_FACTOR + 1,
        -outline => $piececolor,
        -fill    => $piececolor
    );

    $self->scale( $idn, 0, 0, $zoom, $zoom );
    $self->bind( $idn, '<Button-1>', [ \&move_piece, $piece, 'n' ] );
    $piece->add_sensor($idn);

    my $ids = $self->createRectangle(
        $xpos * $SIZE_FACTOR + 1,
        ( $ypos + $sy ) * $SIZE_FACTOR - 1,
        ( $xpos + $sx ) * $SIZE_FACTOR - 1,
        ( $ypos + $sy ) * $SIZE_FACTOR - $OFFSET,
        -outline => $piececolor,
        -fill    => $piececolor
    );

    $self->scale( $ids, 0, 0, $zoom, $zoom );

    $self->bind( $ids, '<Button-1>', [ \&move_piece, $piece, 's' ] );
    $piece->add_sensor($ids);

    my $idw = $self->createRectangle(
        $xpos * $SIZE_FACTOR + $OFFSET,
        $ypos * $SIZE_FACTOR + 1,
        $xpos * $SIZE_FACTOR + 1,
        ( $ypos + $sy ) * $SIZE_FACTOR - 1,
        -outline => $piececolor,
        -fill    => $piececolor
    );

    $self->scale( $idw, 0, 0, $zoom, $zoom );

    $self->bind( $idw, '<Button-1>', [ \&move_piece, $piece, 'w' ] );
    $piece->add_sensor($idw);

    my $ide = $self->createRectangle(
        ( $xpos + $sx ) * $SIZE_FACTOR - 1,
        $ypos * $SIZE_FACTOR + 1,
        ( $xpos + $sx ) * $SIZE_FACTOR - $OFFSET,
        ( $ypos + $sy ) * $SIZE_FACTOR - 1,
        -outline => $piececolor,
        -fill    => $piececolor
    );

    $self->scale( $ide, 0, 0, $zoom, $zoom );
    $self->bind( $ide, '<Button-1>', [ \&move_piece, $piece, 'e' ] );
    $piece->add_sensor($ide);
    return;
}

sub move_piece {
    my ( $self, $piece, $direction, $replay ) = @_;

    my $zoom  = $self->cget('-zoom');
    my $board = $self->cget('-board');

    my $delta = $board->move( $piece, $direction );
    if(not $delta) { return; }

    if ( not defined $replay ) {
        $self->cget('-game')->add_move( $piece->{name}, $direction );
    }

    my $dx = $delta->[0] * $SIZE_FACTOR * $zoom;
    my $dy = $delta->[1] * $SIZE_FACTOR * $zoom;
    $self->move( $piece->get_id(), $dx, $dy );
    foreach my $sensor ( $piece->get_sensors() ) {
        $self->move( $sensor, $dx, $dy );
    }
    if ( $board->check_solution( $self->cget('-game')->get_target() ) ) {
        $self->messageBox(
            -type    => 'OK',
            -icon    => 'info',
            -message => " CONGRATULATIONS!!\n You found the solution."
        );
    }
    return;
}

sub replay_move {
    my ( $self, $game ) = @_;

    my $board = $self->cget('-board');
    my $move  = $game->play_move();
    if ($move) {
        $self->move_piece( $board->{pieces}->{ $move->{name} },
            $move->{direction}, 1 );

        $self->after( $REPLAY_TIME_STEP, [ \&replay_move, $self, $game ] );
    }
    return;
}

1;